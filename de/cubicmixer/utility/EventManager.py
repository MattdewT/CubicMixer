import hardware
import time
import utility


class EventManger:

    '''
    The EventManger gives a central point, to notify the user about (unwanted) events. It provides also an option, to
    handle special cases, like an pending user input.
    '''

    def __init__(self, ns):
        """
        :param ns: shared namespace
        """
        ns.event_state = "standard"                             # setup user input variables, notice that they are not class variables
        ns.pending_user_input_received = False                  # they are shared namespace variables, to make them accessible from every process
        ns.pending_user_input_result = None

    def call_event(self, event, sleep_duration=1, *args):
        """
        call_event starts the event handler function corresponding the event type. After execution, it holds for a
        defined time.
        :param event: String, that contains the event to call
        :param sleep_duration: sleep duration after event execution
        :param args: any parameters that are needed for the event
        """
        if args:                                                                    # handle events with arguments
            if event == "dice_rolled":
                self.handle_event_display_roll_result(args[0])
            elif event == "scripts_loaded":
                self.handle_event_scripts_loaded(args[0], args[1])
            elif event == "mix_request":
                self.handle_mix_request(args[0])
        else:                                                                       # handle events with no arguments
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
            
        time.sleep(sleep_duration)                                                  # hold executor process after event handle for defined time

    def return_lambda_namespace_callback(self, ns, ui):
        """
        Generates a lambda for the button callback. The lambda is needed to save the arguments of button event handler.
        This makes every shared variable in the namespace available for the button interrupts.
        :param ns: shared namespace
        :param ui: user interface object
        :return: lambda function for the button callback
        """
        return lambda channel: self.handle_event_button_pressed(ns, ui, channel)

    @staticmethod
    def handle_event_start_up():
        """
        Display a small start up messages
        """
        hardware.Display.write_display(["Start up", "Message"])

    @staticmethod
    def handle_event_cube_connected():
        """
        Notifies, that the cube has connected over tcp
        """
        hardware.Display.write_display(["Cube", "connected"])

    @staticmethod
    def handle_event_cube_disconnected():
        """
        Notifies, that the cube has disconnected over tcp
        """
        hardware.Display.write_display(["Cube", "disconnected"])

    @staticmethod
    def handle_event_dice_rolling():
        """
        Notifies, when the cube is moving
        """
        hardware.Display.write_display(["Dice", "is rolling"])

    @staticmethod
    def handle_event_display_roll_result(dice_throw_result):
        """
        Display the dice roll result on the lcd.
        :param dice_throw_result: dice roll result
        """
        hardware.Display.write_display(["you've rolled a", str(dice_throw_result)])

    def handle_event_button_pressed(self, ns, ui, channel):
        """
        Handles any buttons interrupts, depending on the current event state.
        :param ns: shared namespace object
        :param ui: user interface object
        :param channel: GPIO channel of the interrupt
        """
        if ns.event_state == "standard":
            utility.UI.update_buttons(ui, channel)                                      # standard button callback
        elif ns.event_state == "mix_request":
            self.handle_event_button_pressed_mix_request(ns, channel)                   # pending user input for mix request

    @staticmethod
    def handle_event_button_pressed_mix_request(ns, channel):
        """
        Fetches the confirmation from the user, to mix the chosen recipe. The program continues only, if the user
        denies or accept the request.
        :param ns: shared namespace object
        :param channel: GPIO channel of the interrupt
        """
        if channel == hardware.IO.pin_enter:
            ns.pending_user_input_received = True
            ns.pending_user_input_result = True
        elif channel == hardware.IO.pin_back:
            ns.pending_user_input_received = True
            ns.pending_user_input_result = False
            hardware.Display.write_display(["Aborting", "..."])

    @staticmethod
    def handle_mix_request(recipe):
        """
        Ask the user, if the chosen recipes should be mixed. Only displays the request, doesnt parse any user inputs
        :param recipe: recipe object to mix
        """
        hardware.Display.write_display(["Mix", recipe.name + "?"])

    @staticmethod
    def handle_serial_error():
        """
        Prompts the user to connect the dice, when the serial connection could not init.
        """
        hardware.Display.write_display(["please connect", "cube over usb"])

    @staticmethod
    def handle_connecting_cube():
        """
        Notifies the user, that the cube now is trying to connect to the wifi.
        """
        hardware.Display.write_display(["connecting", "cube with wifi"])

    @staticmethod
    def handle_cube_configured():
        """
        Notifies the user, that the cube has connected successfully.
        """
        hardware.Display.write_display(["cube configured", "and connected"])

    @staticmethod
    def handle_event_scripts_loaded(ic, rc):
        """
        Gives a quick summary for the user about the loaded scripts.
        :param ic: quantity of loaded ingredients
        :param rc: quantity of loaded recipes
        """
        hardware.Display.write_display(["Ingredients: " + str(ic), "Recipes: " + str(rc)])



