import hardware
import Dice


class Mixer:

    def __init__(self, library):
        self.ingredient_key_size = dict()
        self.ingredient_key_alternator = dict()
        for key in library.ingredients_dict:
            self.ingredient_key_size[key] = len(library.ingredients_dict[key])
            self.ingredient_key_alternator[key] = 0

    def mix_drink(self, recipe, library):
        hardware.Display.write_display(["Mixing:", recipe.name])

        valve_volume_dict = dict()
        for ingredient in recipe.ingredients:
            condiment = ingredient[0]
            volume = ingredient[1]

            valves = library.ingredients_dict[condiment]
            valve_volume_dict[valves[self.ingredient_key_alternator[condiment]]] = volume
            self.ingredient_key_alternator[condiment] += 1
            if self.ingredient_key_alternator[condiment] == self.ingredient_key_size[condiment]:
                self.ingredient_key_alternator[condiment] = 0

        return valve_volume_dict

    @staticmethod
    def chose_recipe(dice_roll_number, library):
        float_ = (float(dice_roll_number) / float((Dice.dice_possible_outcomes + 1))) * len(library.recipes_list)
        return int(float_)
