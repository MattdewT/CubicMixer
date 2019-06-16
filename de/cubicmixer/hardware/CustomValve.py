from ValveInterface import ValveInterface
import IO
from utility import Diagnostic
import time


class Tank:

    def __init__(self, volume, base_area, valve_number, pipe_diameter):
        self.volume = volume
        self.base_area = base_area
        self.valve_number = valve_number
        self.pipe_diameter = pipe_diameter

    def subtract_volume(self, volume):
        self.volume -= volume
        print Diagnostic.debug_str, "Tank Nr.", self.valve_number, "Volume: ", self.volume, Diagnostic.bcolors.ENDC

    def get_height_of_liquid(self):
        height = self.volume / self.base_area
        return height

    def compensate_pipe(self):
        height_outside_liquid = 340 - self.get_height_of_liquid()
        pipe_volume = height_outside_liquid * (0.5 * self.pipe_diameter) ** 2 * 3.14159265359
        return pipe_volume * 0.001


'''Every Valve class need to define get_postion functions that returns the valve position
as int and an open(float) function'''


class Valve(ValveInterface):

    def __init__(self, position, pin, pump_factor=400/11):
        self.position = position
        self.pin = pin
        self.container = Tank(400, 100000 / 33 , position, 6)
        self.pump_factor = pump_factor
        IO.set_pinmode(pin, "out")
        IO.set_pin(pin, "LOW")

    def open(self, volume):
        volume_to_dispense = volume + self.container.compensate_pipe()
        self.dispense_volume(volume_to_dispense)
        self.container.subtract_volume(volume)

    def dispense_volume(self, volume):
        IO.set_pin(self.pin, "HIGH")
        print "volume:", volume
        print "time:", volume  / self.pump_factor
        time.sleep(volume  / self.pump_factor)
        IO.set_pin(self.pin, "LOW")

    def get_position(self):
        return self.position


def setup_valve():
    valves =[Valve(1, 5),
             Valve(2, 6),
             Valve(3, 13),
             Valve(4, 26)]

    return valves
