from utility import Diagnostic


# input [first_line (String), second_line(String)]
def write_display(msg):        # ToDO proper checkign and structering
    if len(msg[0]) > 16 or len(msg[1]) > 16:
        print Diagnostic.debug_str + "message to long to diplay on lcd: ", msg, Diagnostic.bcolors.ENDC
    print Diagnostic.display_str + msg[0] + Diagnostic.bcolors.ENDC
    print Diagnostic.display_str + msg[1] + Diagnostic.bcolors.ENDC

