'''
Created on 24.05.2019

@author: pi
'''
# import RPi.GPIO as GPIO


def setup_gpio(ns, ui):
    
    callback_lambda = ns.em.return_lambda_namespace_callback(ns, ui)

    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(17, GPIO.RISING, callback=callback_lambda, bouncetime=250)
    GPIO.add_event_detect(18, GPIO.RISING, callback=callback_lambda, bouncetime=250)
    GPIO.add_event_detect(19, GPIO.RISING, callback=callback_lambda, bouncetime=250)
    GPIO.add_event_detect(20, GPIO.RISING, callback=callback_lambda, bouncetime=250)
    

def setup_keyboard(ns, ui):
    pass