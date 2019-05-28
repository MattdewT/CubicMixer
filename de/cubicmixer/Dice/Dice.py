import socket
from utility import Diagnostic
import errno
from socket import error as socket_error
import time


class DiceData:

    def __init__(self, orientation, is_rolling):
        self.orientation = orientation
        self.is_rolling = is_rolling


class Dice:

    def __init__(self):
        self.idle_counter = 0
        self.values = [0, 0, 0]
        self.old_values = [0, 0, 0]
        self.delta = [0, 0, 0]

    def parse_content(self, c):
        array = c.split(" ")
        ax = float(array[1])
        ay = float(array[3])
        az = float(array[5])

        self.values = [ax, ay, az]

    def calculate_delta(self):
        delta = [0, 0, 0]

        for i in range(0, 2):
            delta[i] = -self.old_values[i] + self.values[i]

        self.delta = delta
        self.old_values = self.values

    def cube_idle_counter(self):
        if self.cube_moved():
            self.idle_counter = 0
        else:
            self.idle_counter += 1

        return self.idle_counter

    def cube_moved(self):
        result = False

        for i in range(0, 2):
            if (self.delta[i] < -0.05) | (self.delta[i] > 0.05):
                result = True

        return result

    def get_orientation(self):
        return [Dice.round_num(self.values[0]), Dice.round_num(self.values[1]), Dice.round_num(self.values[2])]

    def get_current_dice_roll_list(self):
        is_dice_rolling = self.idle_counter > 5

        return is_dice_rolling, self.get_orientation()

    def get_current_dice_roll_object(self):
        is_dice_rolling = self.idle_counter > 5

        return DiceData(self.get_orientation(), is_dice_rolling)

    @staticmethod
    def round_num(n):
        result = 0

        if n > 0.9:
            result = 1
        elif n < -0.9:
            result = -1

        return result


def convert_to_dice_numbers(xyz):
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


def run(ns):

    TCP_IP = '192.168.137.225'

    TCP_PORT = 80
    BUFFER_SIZE = 1024

    d = Dice()
    dice_connected_first_time = True

    while ns.running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)                                             # socket timeout
            s.connect((TCP_IP, TCP_PORT))

            if dice_connected_first_time:
                print Diagnostic.debug_str + "Dice connected" + Diagnostic.bcolors.ENDC
                dice_connected_first_time = False
                ns.em.call_event("cube_connected", 0)

            data = s.recv(BUFFER_SIZE)

            d.parse_content(data)
            d.calculate_delta()
            d.cube_idle_counter()
            ns.dice_data = d.get_current_dice_roll_object()

            s.close()
        except socket.timeout as e:
            if not dice_connected_first_time:
                print Diagnostic.debug_str + "Dice disconnected" + Diagnostic.bcolors.ENDC
                ns.em.call_event("cube_disconnected", 0)
            dice_connected_first_time = True
        except socket_error as serr:
            if serr.errno == errno.ECONNREFUSED:
                print Diagnostic.error_str + "couldn't connected to cube, retrying in 30 seconds" + Diagnostic.bcolors.ENDC
                time.sleep(30)


