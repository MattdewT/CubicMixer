import scripts
import os
from utility import Diagnostic
import hardware
from utility.Mixer import Mixer
import utility
from multiprocessing import Process, Manager
import Dice
import time

if __name__ == "__main__":

    # --------------------------------------- setup multiprocessing namespace -----------------------------

    mgr = Manager()
    ns = mgr.Namespace()

    # --------------------------------------------- event manager -----------------------------------------------------

    ns.em = utility.EventManger()
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

    # --------------------------------- test n stuff ------------------------------------

    hardware.Display.write_display(["Ingredients: " + str(len(scripts.library.ingredients_dict)), "Recipes: " + str(len(scripts.library.recipes_list))])

    print Diagnostic.separator_str

    print Diagnostic.unloaded_scripts, "unloaded scripts"
    print Diagnostic.discarded_recipe, "discarded recipes"
    print Diagnostic.discarded_ingredients, "discarded ingredients"

    mixer = Mixer()

    print mixer.mix_drink(scripts.library.recipes_list[0]), "Mix 1"
    vc = hardware.Valve_Master.setup_valve_controller()
    vc.open_valves(mixer.mix_drink(scripts.library.recipes_list[0]))

    # --------------------------------- dice connection process setup ------------------------------------

    ns.dice_data = Dice.DiceData([0, 0, 0], False)
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

    print Diagnostic.separator_str

    d = ns.em.return_lambda_namespace_callback(ns)
    d(2)

    print Diagnostic.separator_str

    # --------------------------------- main loop ------------------------------------

    while ns.running:

        # -------------------------------------------- slow down main loop ---------------------------------------------
        time.sleep(0.2)
        # ------------------------------------------- get dice rolls ---------------------------------------------------
        if not ns.dice_data.is_rolling:
            cubed_changed = True
        if cubed_changed and ns.dice_data.is_rolling:
            cubed_changed = False
            print ns.dice_data.orientation, ns.dice_data.is_rolling, Dice.convert_to_dice_numbers(ns.dice_data.orientation)
            #mixer.chose_recipe(Dice.convert_to_dice_numbers(ns.dice_data.orientation))
        # ------------------------------------------ gui user interface ------------------------------------------------
        #utility.UI.update(TestUI)

    # ---------------------------------------- clean up and shutdown ---------------------------------------------------

    p.join()




