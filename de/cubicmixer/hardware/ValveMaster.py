import CustomValve


def setup_valve_controller():
    vc_ = ValveController()

    valve_list = CustomValve.setup_valve()

    for valves in valve_list:
        vc_.add_valve(valves)

    return vc_


class ValveController:

    def __init__(self):
        self.valve_dict = dict()

    def add_valve(self, valve_to_add):
        self.valve_dict[valve_to_add.get_position()] = valve_to_add

    def open_valves(self, order_dict):          #ToDo Proper naming
        print order_dict
        for key in order_dict:
            self.valve_dict[key].open(order_dict[key])

