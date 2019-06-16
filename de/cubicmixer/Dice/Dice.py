import socket
from utility import Diagnostic
import errno
from socket import error as socket_error
import time
import serial
import platform


'''
The dice module handles everything about the wireless dice input. It connects the cube with wifi and starts a tcp
connection. After that the received data get parsed and shared over the multiprocessing namespace. In this documentation
the wireless dice is referred as dice or cube.
'''


class DiceData:

    '''DiceData
    DiceData represents the current state of the dice. The current state is defined by current orientation as list
    [x,y,z] as rounded values of 1, 0 and -1 and if it's still rolling. DiceDate is used as an encapsulation of the
    dice data for the shared namespace.
    '''

    def __init__(self, orientation, is_not_rolling):
        self.orientation = orientation
        self.is_not_rolling = is_not_rolling


class Dice:

    '''
    The Dice class holds all function, for parsing and transforming the received data from the tcp connection
    '''

    def __init__(self):
        self.idle_counter = 0
        self.values = [0, 0, 0]                 # acceleration in x,y and z as floats
        self.old_values = [0, 0, 0]
        self.delta = [0, 0, 0]                  # delta between the current values and old values as float

    def reset_cube(self, c):

        '''
        This function reset the cube on connection, so that no event is triggered by the newly connected cube.
        :param c: the input string from the initial tcp connection
        '''

        self.idle_counter = 5           # set cube as idle
        self.parse_content(c)           # set current values
        self.calculate_delta()          # set old values
        self.delta = [0, 0, 0]          # reset delta

    def parse_content(self, c):

        '''
        parse_content parses the received string from the dice. An example string would be "Ax: 0.01 Ay: 1.02 Az: -0.02"
        and parses to [0.01, 1.02, -0.02].
        :param c: input string from the tcp connection
        '''

        array = c.split(" ")                    # separate by single space
        ax = float(array[1])
        ay = float(array[3])
        az = float(array[5])

        self.values = [ax, ay, az]

    def calculate_delta(self):

        '''
        calculate_delta calculates the delta between the old values and the current values. Following the old values get
        updated.
        '''

        delta = [0, 0, 0]

        for i in range(0, 2):
            delta[i] = -self.old_values[i] + self.values[i]

        self.delta = delta
        self.old_values = self.values

    def cube_idle_counter(self):

        '''
        uses the previously calculate information, if the cube has moved, to count the idle time
        :return: returns the time the cube have not moved in iteration
        '''

        if self.cube_moved():
            self.idle_counter = 0
        else:
            self.idle_counter += 1

        return self.idle_counter

    def cube_moved(self):

        '''
        detects motion of the dice, with the calculated delta values of calculate_delta()
        :returns: True if the cube has moved
        '''

        sensitivity = 0.05                          # sensitivity in g to trigger motion detection
        result = False

        for i in range(0, 2):
            if (self.delta[i] < -sensitivity) | (self.delta[i] > sensitivity):
                result = True

        return result

    def get_orientation(self):

        '''
        Getter for the orientation of the cube.
        :returns: List with x,y,z orientation of cube as -1, 0 or 1
        '''

        return [Dice.round_num(self.values[0]), Dice.round_num(self.values[1]), Dice.round_num(self.values[2])]

    def get_current_dice_roll_list(self):

        '''
        Gives the current status of the dice as list
        :returns: dice status as list [is_dice_rolling, orientation[x,y,z]]
        '''

        is_dice_rolling = self.idle_counter > 5

        return is_dice_rolling, self.get_orientation()

    def get_current_dice_roll_object(self):

        '''
        Gives the current status of the dice as a DiceData object
        :returns: A DiceData object
        '''

        is_dice_rolling = self.idle_counter > 5

        return DiceData(self.get_orientation(), is_dice_rolling)

    @staticmethod
    def round_num(n):

        '''
        Rounds the raw input of the dice accelerometer to clear values of -1, 0 or 1
        :param n: raw acceleration value
        :returns: rounded value of -1, 0 or 1
        '''

        result = 0

        if n > 0.9:
            result = 1
        elif n < -0.9:
            result = -1

        return result


def convert_to_dice_numbers(xyz):

    '''
    Uses the orientation vector to calculate a dice side
    :param xyz: orientation as list [x,y,z]
    :return: a representative dice of 1 to 6, or None if not definite
    '''

    if xyz[0] == -1:
        return 1
    elif xyz[0] == 1:
        return 6
    elif xyz[1] == -1:
        return 3
    elif xyz[1] == 1:
        return 4
    elif xyz[2] == -1:
        return 2
    elif xyz[2] == 1:
        return 5
    else:
        print Diagnostic.debug_str + "could not assign face" + Diagnostic.bcolors.ENDC


def get_serial_connection(ns):

    '''
    Sets up a serial connection with the cube over USB.
    :param ns: shared namespace
    :return: serial connection to the dice
    '''

    serial_running = False
    ser = None
    com_port = 'COM2' if platform.system() == "Windows" else '/dev/ttyUSB0'         # windows and linux have different serial connection definitions

    while not serial_running:                                       # keep trying until serial connection is running
        try:
            if platform.system() == "Linux":
                ser = serial.Serial(com_port, 115200)
                serial_running = True
            elif platform.system() == "Windows":
                ser = serial.Serial(com_port, 115200)
                serial_running = True
        except serial.SerialException:                              # catch missing usb connection
            ns.em.call_event("serial_error", 2)                     # notify user that no cube has be found

    return ser


def setup_wireless_connection(ns):

    '''
    Uses the serial communication with the cube to connected it to a specified wireless network. The cube returns his ip
    address in the wireless network can be disconnected from the host computer. WLAN SSID and password  are defined in
    the function body in clear text.
    :param ns: shared namespace
    :returns: the ip address of the connected dice in the specified wlan network
    '''

    ip = None
    cube_connected = False

    wlan_ssid = "CubeNet"                                                           # wlan ssid
    wlan_password = "CubicMixer"                                                       # wlan password

    ser = get_serial_connection(ns)                                             # setup the serial communication

    ns.em.call_event("connecting_cube")                                         # notify user over successfully serial connection
        
    while not cube_connected:                                                   # wait for cube to connect to the wifi
        line = ser.readline()
        line.rstrip()
        print line
        if line == "SSID\r\n":                                                  # transmit wlan ssid
            ser.write(wlan_ssid)
        elif line == "Password\r\n":                                            # transmit wlan password
            ser.write(wlan_password)
        elif len(line.split(" ")) > 2:
            if len(line.split("IP:")) > 1:
                cube_connected = True
                ip_raw = str(line.split("IP:")[1])                              # parse ip from received message
                ip = ip_raw.rstrip()
    
    ns.em.call_event("cube_configured")                                         # notify user over successfully connection to wifi

    print Diagnostic.debug_str + "dice connected with the ip:",ip, Diagnostic.bcolors.ENDC
    return str(ip)


def run(ns):

    '''
    Sets up the tcp connection to the cube and parses the received messages and shares the created dice status over the
    shared namespace.
    :param ns: shared namespace
    '''

    if ns.emulate_dice:                                             # skip if dice should be emulated
        return
    
    TCP_IP = setup_wireless_connection(ns)                          # connect cube to wifi and fetch ip
        
    TCP_PORT = 80
    BUFFER_SIZE = 1024

    d = Dice()
    dice_connected_first_time = True                                # needed to generate user information

    while ns.running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # start tcp connection
            s.settimeout(5)                                         # socket timeout
            s.connect((TCP_IP, TCP_PORT))
            data = s.recv(BUFFER_SIZE)                              # receive data

            if dice_connected_first_time:                           # notify user about wireless dice connection
                print Diagnostic.debug_str + "Dice connected" + Diagnostic.bcolors.ENDC
                dice_connected_first_time = False
                ns.em.call_event("cube_connected", 0)
                d.reset_cube(data)
            else:                                                   # parse data
                d.parse_content(data)
                d.calculate_delta()
                d.cube_idle_counter()
                ns.dice_data = d.get_current_dice_roll_object()     # share dice status over namespace

                s.close()                                           # close connection
        except socket.timeout:
            if not dice_connected_first_time:
                print Diagnostic.debug_str + "Dice disconnected" + Diagnostic.bcolors.ENDC
                ns.em.call_event("cube_disconnected", 0)            # notify over dice disconnect
            dice_connected_first_time = True
        except socket_error as serr:
            if serr.errno == errno.ECONNREFUSED:
                print Diagnostic.error_str + "couldn't connected to cube, retrying in 30 seconds" + Diagnostic.bcolors.ENDC
                time.sleep(30)
