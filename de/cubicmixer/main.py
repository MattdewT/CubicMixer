import scripts
import os
import sys
from utility import Diagnostic
import hardware
from utility.Mixer import Mixer
import utility
from multiprocessing import Process, Manager, Lock
import Dice
import time


def dice_loop(namespace, mixer_, library, valve_controller):

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

            valve_controller.open_valves(mixer_.handle_dice_roll(dice_roll_number, namespace.mix_by_recipes, library))


def ui_loop(namespace, ui):

    while namespace.running:
        if namespace.keyboard_input:
            # -------------------------------------------- slow down ui loop -------------------------------------------
            time.sleep(0.2)
            # ------------------------------------------- update ui ---------------------------------------------------
            utility.UI.update_keyboard(ui, namespace)


if __name__ == "__main__":

    # --------------------------------------- setup multiprocessing namespace -----------------------------

    mgr = Manager()
    ns = mgr.Namespace()

    # --------------------------------------- parse script parameters -----------------------------

    ns.keyboard_input = False
    ns.emulate_dice = False

    for args in sys.argv:
        if args == 'd':
            ns.emulate_dice = True
        elif args == 'k':
            ns.keyboard_input = True

    # --------------------------------------------- event manager -----------------------------------------------------

    ns.em = utility.EventManger()

    # --------------------------------- hardware setup ------------------------------------
    
    hardware.IO.setup_gpio_configuration()
    display = hardware.Display.Display()
    display.setup()

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

    ns.em.call_event("scripts_loaded", 1, len(scripts.library.ingredients_dict), len(scripts.library.recipes_list))
    # --------------------------------- setup mixer and valve controller ------------------------------------

    mixer = Mixer(scripts.library)
    hardware.ValveMaster.vc = hardware.ValveMaster.setup_valve_controller()

    # --------------------------------- setup UI ------------------------------------

    print Diagnostic.separator_str

    UI_ = utility.UI.UserInterface(utility.UI.Config(ns, hardware.ValveMaster.vc, scripts.library))

    UI_.UITree.print_tree()

    UI_.UITree.go_to_root()
    UI_.UITree.descend(0)

    hardware.IO.setup(ns, UI_)

    print Diagnostic.separator_str

    print Diagnostic.separator_str

    # --------------------------------- dice connection process setup ------------------------------------

    ns.dice_data = Dice.DiceData([0, 0, 0], True)
    ns.running = True

    p = Process(target=Dice.run, args=(ns, ))
    p.start()

    d = Process(target=dice_loop, args=(ns, mixer, scripts.library, hardware.ValveMaster.vc))
    d.start()

    # --------------------------------- main loop ------------------------------------

    ui_loop(ns, UI_)

    # ---------------------------------------- clean up and shutdown ---------------------------------------------------

    ns.running = False
    p.join()
    d.join()
    hardware.IO.clean_up()







