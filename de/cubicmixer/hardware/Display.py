from utility import Diagnostic
import platform
import time
if not platform.system() == "Windows":
    import LCD1602


# input [first_line (String), second_line(String)]
def write_display(msg):        # ToDO proper checkign and structering
    if len(msg[0]) > 16 or len(msg[1]) > 16:
        print Diagnostic.debug_str + "message to long to diplay on lcd: ", msg, Diagnostic.bcolors.ENDC
    print Diagnostic.display_str + msg[0] + Diagnostic.bcolors.ENDC
    print Diagnostic.display_str + msg[1] + Diagnostic.bcolors.ENDC

    if not platform.system() == "Windows":
        LCD1602.clear()
        LCD1602.write(0, 0, msg[0])
        LCD1602.write(0, 1, msg[1])


def setup():
    if platform.system() == "Windows":
        print Diagnostic.warning_str + "Running on a windows system, any IO will be simulated" + Diagnostic.bcolors.ENDC
    else:
        LCD1602.init(0x27, 1)    # init(slave address, background light)
        LCD1602.write(0, 0, 'Greetings!!')
        LCD1602.write(1, 1, 'from SunFounder')
        time.sleep(2)

