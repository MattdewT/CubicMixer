import abc


class ValveInterface:

    '''
    ValveInterface that helps the user to create own custom valves module. As long the custom valve inheritance the
    ValveInterface, the ValveMaster can interact with it.
    '''

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def open(self, volume):

        '''
        should activated the valve to dispense the specified volume
        :param volume: volume to dispense by the valve
        '''

        raise NotImplementedError

    @abc.abstractmethod
    def get_position(self):

        '''
        should return the digital position of the valve, it doesnt need to be the connected pin of the valve
        '''

        raise NotImplementedError
