""""CubicMixer script description

Project description:
    CubicMixer is a mixing automat based on an random dice input. The dice is connected over WiFi with Raspberry Pi on
    transmit automatically the thrown dice result. Based on this random generated number, a recipe scripts gets chosen
    and executed. Those scripts uses an own programming language to parse and compile recipes and ingredients. This
    enable a simple extension of the mixer capabilities without changing to python source code.

Main module description:
    The main module initialises the script and starts all subthreads. Important files with the key functuality for the
    mixing are: "/Dice/Dice.py", "/hardware/CustomValves.py", "/hardware/ValveMaster.py" and "/utility/Mixer.py"

    Important files for the loading and parsing of the custom recipe and ingredients scripts are: "/scripts/FileIO.py",
    "/script/Library.py" and "/scripts/EBNF/Automat.py"

Run parameters
    k:  Enables keyboard input to simulate button inputs
        a = Left, d = Right, w = Enter, s = Back
    d:  Enables dice simulation with the keys 1 to 6. Keyboard input have to be activated for this to work.
"""

import scripts
from utility import Diagnostic
import Dice
import hardware
from utility.Mixer import Mixer
import utility

from multiprocessing import Process, Manager
import time
import os
import sys


def dice_loop(namespace, mixer_, library):

    """dice_loop

    The dice loop register any movement of the cube and determines the thrown result. When a dice result gets
    registered, the loop starts the mixer and  hands over all needed parameters.

    :param namespace: shared variable namespace to pass different parameters between subthreads
    :param mixer_: mixer instance to executed recipe scripts
    :param library: library instance that holds all loaded recipes and ingredients
    """

    cube_changed = False

    while namespace.running:

        # -------------------------------------------- slow down dice loop ---------------------------------------------
        time.sleep(0.2)
        # ------------------------------------------- get dice rolls ---------------------------------------------------
        if not namespace.dice_data.is_not_rolling:
            cube_changed = True
            namespace.em.call_event("dice_rolling", 1)

        if cube_changed and namespace.dice_data.is_not_rolling:
            cube_changed = False

            dice_roll_number = Dice.convert_to_dice_numbers(namespace.dice_data.orientation)

            print namespace.dice_data.orientation, namespace.dice_data.is_not_rolling, str(dice_roll_number)
            namespace.em.call_event("dice_rolled", 1, dice_roll_number)

            namespace.event_state = "mix_request"
            namespace.em.call_event("mix_request", 1, library.recipes_list[mixer_.chose_recipe(dice_roll_number, library)])

            while not namespace.pending_user_input_received:
                pass
            namespace.pending_user_input_received = False
            mix_request = namespace.pending_user_input_result
            namespace.event_state = "standard"

            if mix_request:
                vc = namespace.vc
                vc.open_valves(mixer_.handle_dice_roll(dice_roll_number, namespace.mix_by_recipes, library))
                namespace.vc = vc                                                                               # update namespace instant


def ui_loop(namespace, ui):

    """"ui_loop

    The ui loop registers any key presses (if the keyboard input activated) and interprets them. Button presses (GPIO)
    are actually handled with an interrupt, so there is no need to interpret them in the ui loop

    :param namespace: shared variable namespace to pass different parameters between subthreads
    :param ui: user interface instance

    """

    while namespace.running:
        if namespace.keyboard_input:
            # -------------------------------------------- slow down ui loop -------------------------------------------
            time.sleep(0.2)
            # ------------------------------------------- update ui ---------------------------------------------------
            utility.UI.update_keyboard(ui, namespace)


if __name__ == "__main__":

    '''main
    In the main all needed instances get generated and initialised. Then the main loops get started.
    '''

    # --------------------------------------- setup multiprocessing namespace -----------------------------

    mgr = Manager()
    ns = mgr.Namespace()

    # --------------------------------------- parse run parameters -----------------------------

    ns.keyboard_input = False
    ns.emulate_dice = False

    for args in sys.argv:
        if args == 'd':
            ns.emulate_dice = True
            print Diagnostic.warning_str + "Dice simulation enabled, use keys 1 to 6 to simulate dice input" + Diagnostic.bcolors.ENDC
        elif args == 'k':
            ns.keyboard_input = True
            print Diagnostic.warning_str + "Keyboard input enabled, use w=enter, s=back, a=left, d=right as button inputs" + Diagnostic.bcolors.ENDC

        if not ns.keyboard_input and ns.emulate_dice:
            print Diagnostic.error_str + "Keyboard input must be enabled for dice simulation" + Diagnostic.bcolors.ENDC

    # --------------------------------- hardware setup ------------------------------------
    
    hardware.IO.setup_gpio_configuration()
    hardware.Display.Display()                                            # generate display instance

    # --------------------------------------------- setup event manager -----------------------------------------------------

    ns.em = utility.EventManger(ns)
    ns.em.call_event("start_up", 1)
    
    # --------------------------------- load and check scripts ------------------------------------

    b = os.listdir(os.path.join(os.getcwd(), 'res'))
    for s in b:
        scripts.FileIO.load_script(os.path.join(os.getcwd(), 'res', s))

    print Diagnostic.separator_str

    # --------------------------------- parse ingredient scripts ------------------------------------

    scripts.parse_ingredient_dict()
    print Diagnostic.separator_str
    print scripts.library.ingredients_dict
    print Diagnostic.separator_str

    # --------------------------------- parse recipe scripts ------------------------------------

    scripts.parse_recipes_list()
    print Diagnostic.separator_str
    print scripts.library.recipes_list
    print Diagnostic.separator_str

    ns.em.call_event("scripts_loaded", 1, len(scripts.library.ingredients_dict), len(scripts.library.recipes_list))         # print the finished loading result on the lcd
    # --------------------------------- setup mixer and valve controller ------------------------------------

    mixer = Mixer(scripts.library)
    ns.vc = hardware.ValveMaster.setup_valve_controller()

    # --------------------------------- setup UI ------------------------------------

    print Diagnostic.separator_str

    UI_ = utility.UI.UserInterface(utility.UI.Config(ns, scripts.library, mixer))

    UI_.UITree.print_tree()

    UI_.UITree.go_to_root()
    UI_.UITree.descend(0)

    hardware.IO.setup(ns, UI_)

    print Diagnostic.separator_str

    print Diagnostic.separator_str

    # --------------------------------- dice connection process setup ------------------------------------

    ns.dice_data = Dice.DiceData([0, 0, 0], True)

    """"
    dice_data represents the fetched dice throw results in the shared name space
    """

    ns.running = True

    """
    running keeps all subthreads running with a while loop 
    """

    p = Process(target=Dice.run, args=(ns, ))
    p.start()                                                                                   # start tcp connection with dice

    # ---------------------------------  start main threads and loops ------------------------------------

    d = Process(target=dice_loop, args=(ns, mixer, scripts.library))
    d.start()                                                                                   # start dice loop

    ui_loop(ns, UI_)                                                                            # start ui loop

    # ---------------------------------------- clean up and shutdown ---------------------------------------------------

    ns.running = False                                                                          # shutdown all running threads
    p.join()
    d.join()                                                                                    # wait for all threads to close
    hardware.IO.clean_up()







