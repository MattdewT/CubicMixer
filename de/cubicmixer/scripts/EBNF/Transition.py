class Transition:

    """
    Transition defines the condition to the next state.
    """

    def __init__(self, c, nS):
        """
        :param c: characters that triggers the transition
        :param nS: next state position
        """
        self.nextState = nS
        self.chars = c

    def check_transition(self, b):
        """
        Checks for transition condition.
        :param b: char  to check
        :return: the next state, if  char was include, -1 if not
        """
        if b in self.chars:
            return self.nextState
        else:
            return -1
