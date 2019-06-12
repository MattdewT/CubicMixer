'''
Created on 24.05.2019

@author: pi
'''
import platform
from utility import Diagnostic
if not platform.system() == "Windows":
    import RPi.GPIO as GPIO


'''
This module encapsulate all GPIO calls, to simplify usage of the IO. It provides functions for IO interactions, that can
be used by the user in the custom valve module.   
'''


def setup(ns, ui):

    '''
    The setup chose the right setup function depending on the OS. If the OS is windows, the shared flag os_is_windows
    gets set.
    :param ns: shared namespace
    :param ui: user interface object
    '''

    if platform.system() == "Windows":
        ns.os_is_windows = True
    else:
        setup_buttons(ns, ui)
        ns.os_is_windows = False


def setup_gpio_configuration():

    '''
    Set GPIO mode to BCM, if the OS is linux.
    '''

    if platform.system() == "Linux":
        GPIO.setmode(GPIO.BCM)


def setup_buttons(ns, ui):

    '''
    Setups the user interface buttons and configures  the callback functions.
    :param ns: shared namespace
    :param ui: user interface object with callback function
    '''

    callback_lambda = ns.em.return_lambda_namespace_callback(ns, ui)        # callback lambda from event manger
    
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(17, GPIO.RISING, callback=callback_lambda, bouncetime=250)
    GPIO.add_event_detect(18, GPIO.RISING, callback=callback_lambda, bouncetime=250)
    GPIO.add_event_detect(19, GPIO.RISING, callback=callback_lambda, bouncetime=250)
    GPIO.add_event_detect(20, GPIO.RISING, callback=callback_lambda, bouncetime=250)


def clean_up():

    '''
    Cleans up the GPIO
    '''

    if platform.system() == "Linux":
        GPIO.cleanup()
    

def set_pinmode(pin, mode):

    '''
    Sets the pin mode for specified pin. Prints debug message on call.
    :param pin: The gpio pin number (BCM)
    :param mode: (type) String : "in" for input and "out" for output
    '''

    if not platform.system() == "Windows":
        GPIO.setup(pin, GPIO.IN if mode == "in" else GPIO.OUT)
    print Diagnostic.debug_str + "set pin " + str(pin) + " as", "input" if mode == "in" else "output", Diagnostic.bcolors.ENDC


def set_pin(pin, value):

    '''
    Sets the pin output for specified pin. Prints debug message on call.
    :param pin: The gpio pin number (BCM)
    :param value: (type) String : "LOW" for logic low and "HIGH" for logic high
    '''

    if not platform.system() == "Windows":
        GPIO.output(pin, GPIO.LOW if value == "LOW" else GPIO.HIGH)
    print Diagnostic.debug_str + "set pin " + str(pin) + " to", value, Diagnostic.bcolors.ENDC