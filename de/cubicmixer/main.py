import scripts
import os
from utility import Diagnostic
import hardware
from utility.Mixer import Mixer
import utility
from multiprocessing import Process, Manager, Lock
import Dice
import time


def dice_loop(namespace, cube_changed):

    while namespace.running:

        # -------------------------------------------- slow down dice loop ---------------------------------------------
        time.sleep(0.2)
        # ------------------------------------------- get dice rolls ---------------------------------------------------
        if not namespace.dice_data.is_rolling:
            cube_changed = True
            namespace.em.call_event("dice_rolling", 1)

        if cube_changed and namespace.dice_data.is_rolling:
            cube_changed = False

            dice_roll_number = str(Dice.convert_to_dice_numbers(namespace.dice_data.orientation))

            print namespace.dice_data.orientation, namespace.dice_data.is_rolling, dice_roll_number
            namespace.em.call_event("dice_rolled", 1, dice_roll_number)


def ui_loop(namespace, ui):

    while namespace.running:
        # -------------------------------------------- slow down ui loop ---------------------------------------------
        time.sleep(0.2)
        # ------------------------------------------- update ui ---------------------------------------------------
        utility.UI.update_keyboard(ui)


if __name__ == "__main__":
    # --------------------------------------- setup multiprocessing namespace -----------------------------

    mgr = Manager()
    ns = mgr.Namespace()

    # --------------------------------------------- event manager -----------------------------------------------------

    ns.em = utility.EventManger()

    # --------------------------------- hardware setup ------------------------------------
    
    hardware.IO.setup_gpio_configuration()
    hardware.Display.setup()
    # hardware.Display.write_display = lambda msg: hardware.Display.write_display_fct(msg, Lock())
    
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

    # --------------------------------- setup mixer and valve controller ------------------------------------

    mixer = Mixer()
    vc = hardware.ValveMaster.setup_valve_controller()

    # --------------------------------- dice connection process setup ------------------------------------

    ns.dice_data = Dice.DiceData([0, 0, 0], True)
    ns.running = True

    p = Process(target=Dice.run, args=(ns, ))
    p.start()

    cubed_changed = False

    d = Process(target=dice_loop, args=(ns, cubed_changed))
    d.start()

    # --------------------------------- setup UI ------------------------------------

    print Diagnostic.separator_str

    TestUI = utility.UI.UserInterface(ns)

    TestUI.UITree.print_tree()

    TestUI.UITree.go_to_root()
    TestUI.UITree.descend(0)
    
    hardware.IO.setup(ns, TestUI)

    print Diagnostic.separator_str

    print Diagnostic.separator_str

    # --------------------------------- main loop ------------------------------------

    ui_loop(ns, TestUI)

    # ---------------------------------------- clean up and shutdown ---------------------------------------------------

    ns.running = False
    p.join()
    d.join()
    hardware.IO.clean_up()







