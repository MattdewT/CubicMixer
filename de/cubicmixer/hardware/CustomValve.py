from ValveInterface import ValveInterface
import IO
import time

'''Every Valve class need to define get_postion functions that returns the valve position
as int and an open(float) function'''


class Valve(ValveInterface):

    def __init__(self, position, pin):
        self.position = position
        self.pin = pin
        IO.set_pinmode(pin, "out")

    def open(self, volume):
        IO.set_pin(self.pin, "HIGH")
        time.sleep(1)
        IO.set_pin(self.pin, "LOW")

    def get_position(self):
        return self.position


def setup_valve():
    valves =[Valve(1, 5),
             Valve(2, 6),
             Valve(3, 13),
             Valve(4, 26)]

    return valves
