from utility import Diagnostic
import platform
import time
from multiprocessing import Lock
if not platform.system() == "Windows":
    import LCD1602

write_display = None

# input [first_line (String), second_line (String)]
class Display:
    
    def __init__(self):
        self.lock_ = Lock()


    def write_display_fct(self, msg):        # ToDO proper checking and structering
        if len(msg[0]) > 16 or len(msg[1]) > 16:
            print Diagnostic.debug_str + "message to long to diplay on lcd: ", msg, Diagnostic.bcolors.ENDC
        print Diagnostic.display_str + msg[0] + Diagnostic.bcolors.ENDC
        print Diagnostic.display_str + msg[1] + Diagnostic.bcolors.ENDC
    
        self.lock_.acquire(True)
        if not platform.system() == "Windows":          # ToDo: Lock doesnt work
            LCD1602.clear()
            LCD1602.write(0, 0, msg[0])
            LCD1602.write(0, 1, msg[1])
        self.lock_.release()
    
    @staticmethod
    def setup():
        if platform.system() == "Windows":
            print Diagnostic.warning_str + "Running on a windows system, any IO will be simulated" + Diagnostic.bcolors.ENDC
        else:
            LCD1602.init(0x27, 1)    # init(slave address, background light)
            time.sleep(2)
    
