from abc import ABCMeta, abstractmethod

class ValveController:

    def __init__(self):
        self.valve_dict = dict()


# Experimentel abstract class
class ValveInterface:
    __metaclass__ = ABCMeta

    def __init__(self, position):
        self.position = position
        super.__init__()

    @abstractmethod
    def open(self):
        raise NotImplementedError


'''Every Valve class need to define an 'position' variable and an open(float) function'''

class Valve(ValveInterface):

    def open(self, volume):
        print "test", self.position, volume



