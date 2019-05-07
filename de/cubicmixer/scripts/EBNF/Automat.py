from State import State
from Transition import Transition
from Diagnostic import InvalidSyntax


class Automat:
    def __init__(self):
        self.currentState = 1
        self.states = {-1: State(-1, False)}

    def add_state(self, e):
        self.states[e.get_state_number()] = e

    def check_string(self, text):
        text_char = list(text)
        for i in range(len(text_char)):
            c = text_char[i]

            self.currentState = self.states[self.currentState].check(c)

            if self.currentState == -1:
                raise InvalidSyntax(i)

        if self.currentState == -1:
            return False
        else:
            return self.states[self.currentState].is_final_state()


def check_syntax(text, a):
    a.currentState = 1
    print text
    result = a.check_string(text)
    print result
    if not result:
        raise InvalidSyntax(-1)


def setup_automat():

    a = Automat()

    s = State(1, False)
    s.add_transition(Transition(['i'], 2))
    s.add_transition(Transition(['r'], 16))

    a.add_state(s)

    s = State(2, False)
    s.add_transition(Transition(['s'], 3))

    a.add_state(s)

    s = State(3, False)
    s.add_transition(Transition(['\n'], 15))

    a.add_state(s)

    s = State(4, False)
    s.add_transition(Transition([' '], 5))
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 4))

    a.add_state(s)

    s = State(5, False)
    s.add_transition(Transition(['V'], 6))

    a.add_state(s)

    s = State(6, False)
    s.add_transition(Transition(['e'], 7))

    a.add_state(s)

    s = State(7, False)
    s.add_transition(Transition(['n'], 8))

    a.add_state(s)

    s = State(8, False)
    s.add_transition(Transition(['t'], 9))

    a.add_state(s)

    s = State(9, False)
    s.add_transition(Transition(['i'], 10))

    a.add_state(s)

    s = State(10, False)
    s.add_transition(Transition(['l'], 11))

    a.add_state(s)

    s = State(11, False)
    s.add_transition(Transition([' '], 12))

    a.add_state(s)

    s = State(12, False)
    s.add_transition(Transition(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 13))

    a.add_state(s)

    s = State(13, True)
    s.add_transition(Transition(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 13))
    s.add_transition(Transition(['\n'], 14))

    a.add_state(s)

    s = State(14, True)
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 4))

    a.add_state(s)

    s = State(15, False)
    s.add_transition(Transition(['\n'], 15))
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 4))

    a.add_state(s)

    s = State(16, False)
    s.add_transition(Transition(['s'], 17))

    a.add_state(s)

    s = State(17, False)
    s.add_transition(Transition(['\n'], 18))

    a.add_state(s)

    s = State(18, False)
    s.add_transition(Transition(['\n'], 18))
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 19))

    a.add_state(s)

    s = State(19, False)
    s.add_transition(Transition(['\n'], 27))
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 19))

    a.add_state(s)

    s = State(20, False)
    s.add_transition(Transition([' '], 21))
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 20))

    a.add_state(s)

    s = State(21, False)
    s.add_transition(Transition(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 22))

    a.add_state(s)

    s = State(22, False)
    s.add_transition(Transition(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 22))
    s.add_transition(Transition([' '], 23))
    s.add_transition(Transition(['m'], 24))

    a.add_state(s)

    s = State(23, False)
    s.add_transition(Transition(['m'], 24))

    a.add_state(s)

    s = State(24, False)
    s.add_transition(Transition(['l'], 25))

    a.add_state(s)

    s = State(25, True)
    s.add_transition(Transition(['\n'], 26))

    a.add_state(s)

    s = State(26, True)
    s.add_transition(Transition(['\n'], 18))
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 20))

    a.add_state(s)

    s = State(27, False)
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 20))
    s.add_transition(Transition(['\n'], 27))

    a.add_state(s)

    return a
