class State:

    """
    State organizes the automat in its own little parts. It holds information about all transition and if it is a
    authorized end condition.
    """

    def __init__(self, state_number, final_state):
        self.state_number = state_number
        self.final_state = final_state
        self.transition = []

    def is_final_state(self):
        """
        Getter for state type
        :return: True, if state is a authorized end condition
        """
        return self.final_state

    def get_state_number(self):
        """
        Getter for the state position.
        :return: State position
        """
        return self.state_number

    def add_transition(self, t):
        """
        Adds transiton to the state.
        :param t: transition to add
        """
        self.transition.append(t)

    def check(self, b):
        """
        Loops through all transition and returns the next state, if a transition applies. If no transition applies, the
        next state is the error state -1.
        :param b: character to check
        :return: th next state
        """
        next_state = -1
        for t in self.transition:
            next_state = t.check_transition(b)
            if next_state != -1:                            # loop until a transition applies or no transition are left
                return next_state
        return next_state
