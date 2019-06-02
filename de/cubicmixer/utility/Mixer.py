import hardware
import Dice


class Mixer:

    def __init__(self, library):
        self.ingredient_key_size = dict()
        self.ingredient_key_alternator = dict()
        for key in library.ingredients_dict:
            self.ingredient_key_size[key] = len(library.ingredients_dict[key])
            self.ingredient_key_alternator[key] = 0

    def mix_drink_recipe(self, recipe, library):
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

    def mix_drink_ingredient(self, ingredient, library):
        hardware.Display.write_display(["adding:", ingredient])

        valve_volume_dict = dict()
        valves = library.ingredients_dict[ingredient]
        valve_volume_dict[valves[self.ingredient_key_alternator[ingredient]]] = mixing_by_ingredients_volume
        self.ingredient_key_alternator[ingredient] += 1
        if self.ingredient_key_alternator[ingredient] == self.ingredient_key_size[ingredient]:
            self.ingredient_key_alternator[ingredient] = 0

        return valve_volume_dict

    def handle_dice_roll(self, dice_roll, mix_by_recipes, library):
        if mix_by_recipes:
            return self.mix_drink_recipe(library.recipes_list[self.chose_recipe(dice_roll, library)], library)
        else:
            return self.mix_drink_ingredient(library.ingredients_dict.keys()[self.chose_ingredient(dice_roll, library)], library)

    @staticmethod
    def chose_recipe(dice_roll_number, library):
        float_ = (float(dice_roll_number) / float((Dice.dice_possible_outcomes + 1))) * len(library.recipes_list)
        return int(float_)

    @staticmethod
    def chose_ingredient(dice_roll_number, library):
        float_ = (float(dice_roll_number) / float((Dice.dice_possible_outcomes + 1))) * len(library.ingredients_dict)
        return int(float_)


mixing_by_ingredients_volume = 50   # ml
