import abc
import CustomValve


class ValveController:

    def __init__(self):
        self.valve_dict = dict()

    def add_valve(self, valve_to_add):
        self.valve_dict[valve_to_add.get_position()] = valve_to_add

    def open_valves(self, order_dict):          #ToDo Proper naming
        for key in order_dict:
            self.valve_dict[key].open(order_dict[key])


def setup_valve_controller():
    vc = ValveController()

    valve_list = CustomValve.setup_valve()

    for valves in valve_list:
        vc.add_valve(valves)

    return vc

vc = None
