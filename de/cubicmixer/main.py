import scripts
import os
from utility import Diagnostic
import hardware
from utility.Mixer import Mixer
import utility

if __name__ == "__main__":

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

    mixer = Mixer()

    print Diagnostic.separator_str

    print Diagnostic.unloaded_scripts, "unloaded scripts"
    print Diagnostic.discarded_recipe, "discarded recipes"
    print Diagnostic.discarded_ingredients, "discarded ingredients"

    print mixer.mix_drink(scripts.library.recipes_list[0]), "Mix 1"
    vc = hardware.Valve_Master.setup_valve_controller()
    vc.open_valves(mixer.mix_drink(scripts.library.recipes_list[0]))

    # --------------------------------- test n stuff UI ------------------------------------

    print Diagnostic.separator_str

    TestUI = utility.UI.UserInterface()
    print TestUI.UITree.current_node.msg
    TestUI.UITree.descend(0)
    print TestUI.UITree.current_node.msg
    TestUI.UITree.descend(0)
    print TestUI.UITree.current_node.msg
    TestUI.UITree.descend(0)
    print TestUI.UITree.current_node.msg
