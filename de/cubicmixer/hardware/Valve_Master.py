import abc


class ValveController:

    def __init__(self):
        self.valve_dict = dict()

    def add_valve(self, valve_to_add):
        self.valve_dict[valve_to_add.get_position()] = valve_to_add

    def open_valves(self, order_dict):          # ToDo Proper naming
        for key in order_dict:
            self.valve_dict[key].open(order_dict[key])


class ValveInterface:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def open(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_position(self):
        raise NotImplementedError


def setup_valve_controller():
    vc = ValveController()
    add_valves_to_controller(vc)
    return vc


'''Every Valve class need to define get_postion functions that returns the valve position as int and an open(float) function'''


class Valve(ValveInterface):

    def __init__(self, position):
        self.position = position

    def open(self, volume):
        print "test", self.position, volume

    def get_position(self):
        return self.position


def add_valves_to_controller(vc):
    vc.add_valve(Valve(9))
    vc.add_valve(Valve(13))