import hardware
import time
import utility


class EventManger:

    '''
    The EventManger gives a central point, to notify the user about (unwanted) events.
    '''

    def __init__(self):
        pass

    def call_event(self, event, sleep_duration=1, *args):
        if args:
            if event == "dice_rolled":
                self.handle_event_display_roll_result(args[0])
            elif event == "scripts_loaded":
                self.handle_event_scripts_loaded(args[0], args[1])
        else:
            if event == "start_up":
                self.handle_event_start_up()
            elif event == "cube_connected":
                self.handle_event_cube_connected()
            elif event == "cube_disconnected":
                self.handle_event_cube_disconnected()
            elif event == "dice_rolling":
                self.handle_event_dice_rolling()
            elif event == "serial_error":
                self.handle_serial_error()
            elif event == "connecting_cube":
                self.handle_connecting_cube()
            elif event == "cube_configured":
                self.handle_cube_configured()
            
        time.sleep(sleep_duration)

    def return_lambda_namespace_callback(self, ns, ui):
        return lambda channel: self.handle_event_button_pressed(ns, ui, channel)

    @staticmethod
    def handle_event_start_up():
        hardware.Display.write_display(["Start up", "Message"])

    @staticmethod
    def handle_event_cube_connected():
        hardware.Display.write_display(["Cube", "connected"])

    @staticmethod
    def handle_event_cube_disconnected():
        hardware.Display.write_display(["Cube", "disconnected"])

    @staticmethod
    def handle_event_waiting_for_input():
        hardware.Display.write_display(["press Enter or ", "roll the dice"])

    @staticmethod
    def handle_event_dice_rolling():
        hardware.Display.write_display(["Dice", "is rolling"])

    @staticmethod
    def handle_event_display_roll_result(dice_throw_result):
        hardware.Display.write_display(["you've rolled a", str(dice_throw_result)])

    @staticmethod
    def handle_event_button_pressed(ns, ui, channel):
        utility.UI.update_buttons(ui, channel)
        
    @staticmethod
    def handle_serial_error():
        hardware.Display.write_display(["please connect", "cube over usb"])
        
    @staticmethod
    def handle_connecting_cube():
        hardware.Display.write_display(["connecting", "cube with wifi"])
    
    @staticmethod
    def handle_cube_configured():
        hardware.Display.write_display(["cube configured", "and connected"])

    @staticmethod
    def handle_event_scripts_loaded(ic, rc):
        hardware.Display.write_display(["Ingredients: " + str(ic), "Recipes: " + str(rc)])



