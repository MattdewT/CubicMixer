from ValveInterface import ValveInterface
import IO
from utility import Diagnostic
import time


'''
There are a lot of different method to dispense a defined amount of liquid. To make this wide range of different method 
available for the user, the source code got separated in his own module to be defined by the user himself. 
In this use case air pumps are used to force the liquid out of solid containers. Therefore a compensation of the empty
pipe is additional necessary.
'''


class Tank:

    '''
    The class Tank represents a cylindrical container, with defined base area and volume. Each tank links to its own
    valve and can be distinguish by their position. To make the fluid dispensation even more accurate, a compensation
    for the pipe was added.
    '''

    def __init__(self, volume, base_area, valve_number, pipe_diameter, high_of_the_pipe):
        """
        Tank represent a simple cylindrical container with a dispense pipe.
        :param volume: Volume of the container
        :param base_area: base surface area of the container
        :param valve_number: valve position number
        :param pipe_diameter: diameter of the dispense pipe
        :param high_of_the_pipe: the high of the dispense pipe, that the fluid needs to overcome
        """
        self.volume = volume
        self.base_area = base_area
        self.valve_number = valve_number
        self.pipe_diameter = pipe_diameter
        self.high_of_the_pipe = high_of_the_pipe

    def subtract_volume(self, volume):
        """
        Removes the volume from the virtual container volume.
        :param volume: Volume that gets dispensed from the container
        """
        self.volume -= volume
        print Diagnostic.debug_str, "Tank Nr.", self.valve_number, "Volume: ", self.volume, Diagnostic.bcolors.ENDC

    def get_height_of_liquid(self):
        """
        Calculates the high of the liquid inside the container
        :return: the high of the liquid inside the container
        """
        height = self.volume / self.base_area
        return height

    def compensate_pipe(self):
        """
        Calculates the part of the pipe that is above the liquid and therefore needs to be filled first.
        :return: the volume of the dispense pipe that needs to be compensated
        """
        height_outside_liquid = self.high_of_the_pipe - self.get_height_of_liquid()
        pipe_volume = height_outside_liquid * (0.5 * self.pipe_diameter) ** 2 * 3.14159265359
        return pipe_volume * 0.001


class Valve(ValveInterface):

    '''
    The Valve class defines the algorithm for operating the valves.
    '''

    def __init__(self, position, pin, pump_factor=400 / 11):
        """
        :param position: virtual position in database
        :param pin: gpio pin number
        :param pump_factor: volume / time
        """
        self.position = position
        self.pin = pin
        self.container = Tank(400, 100000 / 33, position, 6, 330)
        self.pump_factor = pump_factor
        IO.set_pinmode(pin, "out")
        IO.set_pin(pin, "LOW")

    def open(self, volume):
        """
        Open the valve to dispense defined amount of fluid with additional pipe compensation.
        :param volume: volume to dispense
        """
        volume_to_dispense = volume + self.container.compensate_pipe()  # add pipe compensation
        self.dispense_volume(volume_to_dispense)
        self.container.subtract_volume(volume)                          # remove volume from the tank

    def dispense_volume(self, volume):
        """
        Opens the valve to dispense defined amount of fluid.
        :param volume: volume to dispense
        """
        IO.set_pin(self.pin, "HIGH")
        print "volume:", volume
        print "time:", volume  / self.pump_factor
        time.sleep(volume  / self.pump_factor)
        IO.set_pin(self.pin, "LOW")

    @property
    def get_position(self):
        """
        Getter for valve position
        :return: database position of valve
        """
        return self.position


def setup_valve():
    """
    This function generates all needed valve and forms them into a list for the valve master.
    :return: a list with all available valves
    """
    valves =[Valve(1, 5),
             Valve(2, 6),
             Valve(3, 13),
             Valve(4, 26)]

    return valves
