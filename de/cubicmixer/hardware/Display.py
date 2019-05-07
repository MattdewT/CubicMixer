from utility import Diagnostic


# input [first_line (String), second_line(String)]
def write_display(msg):        #ToDO proper checkign and structering
    print Diagnostic.display_str + msg[0] + Diagnostic.bcolors.ENDC
    print Diagnostic.display_str + msg[1] + Diagnostic.bcolors.ENDC

