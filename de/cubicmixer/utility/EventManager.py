import hardware
import time


class EventManger:

    def __init__(self):
        self.event_switch = dict()
        self.event_switch["start_up"] = self.handle_event_start_up

    def call_event(self, event, sleep_duration, *args):
        if args:
            self.event_switch[event](args)
        else:
            self.event_switch[event]()
        time.sleep(sleep_duration)

    @staticmethod
    def handle_event_start_up():
        hardware.Display.write_display(["Start up", "Message"])

    @staticmethod
    def handle_event_cube_connected():
        hardware.Display.write_display(["Cube", "connected"])

    @staticmethod
    def handle_event_cube_disconnect():
        hardware.Display.write_display(["Cube", "disconnected"])

    @staticmethod
    def handle_event_scripts_loaded():
        hardware.Display.write_display(["Script loading", "Done"])

    @staticmethod
    def handle_event_waiting_for_input():
        hardware.Display.write_display(["press Enter or ", "roll the dice"])

    @staticmethod
    def handle_event_dice_rolling():
        hardware.Display.write_display(["Dice", "is rolling"])

    @staticmethod
    def handle_event_display_roll_result(dice_throw_result):
        hardware.Display.write_display(["your rolled a", str(dice_throw_result[0])])


