from utility import Diagnostic
import platform
import time
from multiprocessing import Lock
if not platform.system() == "Windows":
    import LCD1602


class Display:
    """
    Display class serves the purpose, to initialise the hardware and handle writing to the lcd. The primary goal was to
    make the display threading safe.
    """

    lock_ = Lock()

    def __init__(self):
        self.setup()

    @staticmethod
    def write_display_fct(msg):
        """
        Writes the passed message to a LCD screen.
        :param msg: needs to be a list, with two entries in String format, the first entry represents the first line of 
                    the display and the second the second ine of the display
        :raises a warning when the message is longer than the display can show (16 characters per line)
        """
        if len(msg[0]) > 16 or len(msg[1]) > 16:
            print Diagnostic.debug_str + "message to long to diplay on lcd: ", msg, Diagnostic.bcolors.ENDC
        print Diagnostic.display_str + msg[0] + Diagnostic.bcolors.ENDC
        print Diagnostic.display_str + msg[1] + Diagnostic.bcolors.ENDC
    
        Display.lock_.acquire(True)
        if not platform.system() == "Windows":
            LCD1602.clear()
            LCD1602.write(0, 0, msg[0])
            LCD1602.write(0, 1, msg[1])
        Display.lock_.release()
    
    @staticmethod
    def setup():
        if platform.system() == "Windows":
            print Diagnostic.warning_str + "Running on a windows system, any IO will be simulated" + Diagnostic.bcolors.ENDC
        else:
            LCD1602.init(0x27, 1)    # init(slave address, background light)
            time.sleep(2)


write_display = Display.write_display_fct  # type: Display().write_display_fct()
"""
write_display is used as an static reference, so it can be called from every position in the script
"""
