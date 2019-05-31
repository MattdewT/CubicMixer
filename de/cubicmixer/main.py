import scripts
import os
from utility import Diagnostic
import hardware
from utility.Mixer import Mixer
import utility
from multiprocessing import Process, Manager, Lock
import Dice
import time


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

    while ns.running:

        # -------------------------------------------- slow down main loop ---------------------------------------------
        time.sleep(0.2)
        # ------------------------------------------- get dice rolls ---------------------------------------------------
        if not ns.dice_data.is_rolling:
            cubed_changed = True
            ns.em.call_event("dice_rolling", 1)

        if cubed_changed and ns.dice_data.is_rolling:
            cubed_changed = False
            
            dice_roll_number = str(Dice.convert_to_dice_numbers(ns.dice_data.orientation))
            
            print ns.dice_data.orientation, ns.dice_data.is_rolling, dice_roll_number
            ns.em.call_event("dice_rolled", 1, dice_roll_number)
            # mixer.chose_recipe(Dice.convert_to_dice_numbers(ns.dice_data.orientation))
        # ------------------------------------------ gui user interface ------------------------------------------------
        #if ns.os_is_windows:
            #utility.UI.update_keyboard(TestUI)

    # ---------------------------------------- clean up and shutdown ---------------------------------------------------

    ns.running = False
    p.join()
    hardware.IO.clean_up()



