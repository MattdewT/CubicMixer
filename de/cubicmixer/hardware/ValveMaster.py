import CustomValve


'''
ValveMaster loads all custom valves and handles the communication of the custom valve module with rest of the script.
This helps the user, that he only has to modify the custom valves module and doesnt need to change anything else, if 
more ingredients are wished.
'''


def setup_valve_controller():

    '''
    Sets up the valve controller for usage in the main
    :return: ValveController object with all specified custom valves
    '''

    vc_ = ValveController()

    valve_list = CustomValve.setup_valve()          # fetch custom valves

    for valves in valve_list:
        vc_.add_valve(valves)                       # add every

    return vc_


class ValveController:

    '''
    The ValveController holds all connected valves and handles the execution of the generated valve_volume_dict
    '''

    def __init__(self):
        self.valve_dict = dict()

    def add_valve(self, valve_to_add):

        '''
        Adds Valve to the valve controller
        :param valve_to_add: the valve to add
        '''

        self.valve_dict[valve_to_add.get_position()] = valve_to_add

    def open_valves(self, order_dict):

        '''
        Open valves with help of a valve_volume_dict. The valve_volume_dict is a dictionary that contains the wished
        valve position as key and the wished volume as value.
        :param order_dict: valve_volume_dict with {valve position :  volume, valve position 2 :  volume, ...}
        '''

        print order_dict
        for key in order_dict:
            self.valve_dict[key].open(order_dict[key])

