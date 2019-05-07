class State:

    def __init__(self, state_number, final_state):
        self.state_number = state_number
        self.final_state = final_state
        self.transition = []

    def is_final_state(self):
        return self.final_state

    def get_state_number(self):
        return self.state_number

    def add_transition(self, t):
        self.transition.append(t)

    def check(self, b):
        next_state = -1
        for t in self.transition:
            next_state = t.check_transition(b)
            if next_state != -1:
                return next_state
        return next_state
