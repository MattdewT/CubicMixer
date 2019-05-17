from State import State
from Transition import Transition
from utility.Diagnostic import InvalidSyntax


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

    s = State(1, False)                                                                                                 #State 1
    s.add_transition(Transition(['i'], 2))                                                                              #if 'i' go to state 2
    s.add_transition(Transition(['r'], 16))                                                                             #if 'r' go to state 16    

    a.add_state(s)

    s = State(2, False)                                                                                                 #State 2        
    s.add_transition(Transition(['s'], 3))                                                                              #if 's' go to state 3

    a.add_state(s)

    s = State(3, False)                                                                                                 #State 3
    s.add_transition(Transition(['\n'], 15))                                                                            #if '\n' go to state 15    

    a.add_state(s)

    s = State(4, False)                                                                                                 #State 4
    s.add_transition(Transition([' '], 5))                                                                              #if ' ' go to state 5
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 4))   #if 'letter' go to state 4

    a.add_state(s)

    s = State(5, False)                                                                                                 #State 5        
    s.add_transition(Transition(['V'], 6))                                                                              #if 'V' go to state 6

    a.add_state(s)

    s = State(6, False)                                                                                                 #State 6
    s.add_transition(Transition(['e'], 7))                                                                              #if 'e' go to state 7

    a.add_state(s)

    s = State(7, False)                                                                                                 #State 7
    s.add_transition(Transition(['n'], 8))                                                                              #if 'n' go to state 8

    a.add_state(s)

    s = State(8, False)                                                                                                 #State 8
    s.add_transition(Transition(['t'], 9))                                                                              #if 't' go to state 9

    a.add_state(s)

    s = State(9, False)                                                                                                 #State 9
    s.add_transition(Transition(['i'], 10))                                                                             #if 'i' go to state 10

    a.add_state(s)

    s = State(10, False)                                                                                                #State 10
    s.add_transition(Transition(['l'], 11))                                                                             #if 'l' go to state 11

    a.add_state(s)

    s = State(11, False)                                                                                                #State 11
    s.add_transition(Transition([' '], 12))                                                                             #if ' ' go t9o state 12

    a.add_state(s)

    s = State(12, False)                                                                                                #State 12
    s.add_transition(Transition(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 13))                                #if '0-9' go to state 13

    a.add_state(s)

    s = State(13, True)                                                                                                 #State 13
    s.add_transition(Transition(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 13))                                #if '0-9' go to state 13
    s.add_transition(Transition(['\n'], 14))                                                                            #if '\n' go to state 14

    a.add_state(s)

    s = State(14, True)                                                                                                 #State 14    
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 4))   #if 'letter' go to state 4

    a.add_state(s)

    s = State(15, False)
    s.add_transition(Transition(['\n'], 15))                                                                            #State 15
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 4))   #if 'letter' go to state 4

    a.add_state(s)

    s = State(16, False)                                                                                                #State 16
    s.add_transition(Transition(['s'], 17))                                                                             #if 's' go to state 17

    a.add_state(s)

    s = State(17, False)                                                                                                #State 17
    s.add_transition(Transition(['\n'], 18))                                                                            #if '\n' go to state 18

    a.add_state(s)

    s = State(18, False)                                                                                                #State 18
    s.add_transition(Transition(['\n'], 18))                                                                            #if '\n' go to state 18
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 19))    #if 'letter' go to state 19

    a.add_state(s)

    s = State(19, False)                                                                                                #State 19
    s.add_transition(Transition(['\n'], 27))                                                                            #if '\n' go to state 27
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 19))    #if 'letter' go to state 19

    a.add_state(s)

    s = State(20, False)                                                                                                #State 20
    s.add_transition(Transition([' '], 21))                                                                             #if ' ' go to state 21
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 20))    #if 'letter' go to state 20

    a.add_state(s)

    s = State(21, False)                                                                                                #State21    
    s.add_transition(Transition(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 22))                                #if '0-9' go to state 22

    a.add_state(s)

    s = State(22, False)                                                                                                #State 22
    s.add_transition(Transition(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 22))                                #if '0-9' go to state 22
    s.add_transition(Transition([' '], 23))                                                                             #if ' ' go to state 23
    s.add_transition(Transition(['m'], 24))                                                                             #if 'm' go to state 24

    a.add_state(s)

    s = State(23, False)                                                                                                #State 23
    s.add_transition(Transition(['m'], 24))                                                                             #if 'm' go to state 24

    a.add_state(s)

    s = State(24, False)                                                                                                #State 24
    s.add_transition(Transition(['l'], 25))                                                                             #if 'l' go to state 25    

    a.add_state(s)

    s = State(25, True)                                                                                                 #State 25
    s.add_transition(Transition(['\n'], 26))                                                                            #if '\n' go to state 26

    a.add_state(s)

    s = State(26, True)                                                                                                 #State 26
    s.add_transition(Transition(['\n'], 18))                                                                            #if '\n' go to state 18
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 20))    #if 'letter' go to state 20

    a.add_state(s)

    s = State(27, False)                                                                                                #State 27
    s.add_transition(Transition(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 20))    #if 'letter' go to state 20
    s.add_transition(Transition(['\n'], 27))                                                                            #if '\n' go to state 27

    a.add_state(s)

    return a
