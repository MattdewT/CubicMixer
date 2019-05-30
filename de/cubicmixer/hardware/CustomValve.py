from ValveInterface import ValveInterface
import IO
import time

'''Every Valve class need to define get_postion functions that returns the valve position
as int and an open(float) function'''


class Valve(ValveInterface):

    def __init__(self, position):
        self.position = position
        IO.set_pinmode(position, "out")

    def open(self, volume):
        IO.set_pin(self.position, "HIGH")
        time.sleep(1)
        IO.set_pin(self.position, "LOW")

    def get_position(self):
        return self.position


def setup_valve():
    list_ = []

    list_.append(Valve(6))
    list_.append(Valve(8))
    list_.append(Valve(9))
    list_.append(Valve(12))
    list_.append(Valve(13))

    return list_
