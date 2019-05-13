from utility import Diagnostic
import LCD1602
import time


# input [first_line (String), second_line(String)]
def write_display(msg):        # ToDO proper checkign and structering
    if len(msg[0]) > 16 or len(msg[1]) > 16:
        print Diagnostic.debug_str + "message to long to diplay on lcd: ", msg, Diagnostic.bcolors.ENDC
    print Diagnostic.display_str + msg[0] + Diagnostic.bcolors.ENDC
    print Diagnostic.display_str + msg[1] + Diagnostic.bcolors.ENDC
    
    LCD1602.clear()
    LCD1602.write(0, 0, msg[0])
    LCD1602.write(0, 1, msg[1])


def setup():
    LCD1602.init(0x27, 1)    # init(slave address, background light)
    LCD1602.write(0, 0, 'Greetings!!')
    LCD1602.write(1, 1, 'from SunFounder')
    time.sleep(2)