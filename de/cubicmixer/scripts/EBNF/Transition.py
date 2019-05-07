class Transition:

    def __init__(self, c, nS):
        self.nextState = nS
        self.chars = c

    def check_transition(self, b):
        if b in self.chars:
            return self.nextState
        else:
            return -1
