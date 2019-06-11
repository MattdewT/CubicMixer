import hardware
import Dice

'''Module description
The Mixer handles the choosing of a recipe, based on the dice input. After that i
'''


class Mixer:

    '''Mixer
    The Mixer handles the choosing of a recipe, based on the dice input. After that, it generates a list with valve
    position and volume. It takes also care of evenly consumption on container with the same ingredient.
    '''

    def __init__(self, library):
        self.ingredient_key_size = dict()
        self.ingredient_key_alternator = dict()
        for key in library.ingredients_dict:                                        # generate alternator for evenly distribution of ingredients with multiple container
            self.ingredient_key_size[key] = len(library.ingredients_dict[key])      # amount of containers per ingredient
            self.ingredient_key_alternator[key] = 0

    def handle_dice_roll(self, dice_roll, mix_by_recipes, library):
        """handle_dice_roll
        handle_dice_roll is the central point, where a recipe is chosen and the valve volume dictionary is generated
        :param mix_by_recipes: boolean to determine the operation mode
        :param library: library with all loaded recipes and ingredients
        :param dice_roll: integer between 1 to 6 that represent the dice roll
        :return dictionary with [valve_position : ingredient_volume]
        """
        if mix_by_recipes:
            return self.mix_drink_recipe(library.recipes_list[self.chose_recipe(dice_roll, library)], library)              # chose recipe and hand over to recipe mixer
        else:
            return self.mix_drink_ingredient(library.ingredients_dict.keys()[self.chose_ingredient(dice_roll, library)],    # chose ingredient and hand over to ingredient mixer
                                             library)

    def mix_drink_recipe(self, recipe, library):

        '''
        generates a volume dictionary for the valve controller based on an input recipe
        :param recipe: recipe object, that contains all information about the recipe
        :param library: library with all loaded ingredients
        :return: dictionary with valve position and volume to dispense [Int:Float]
        '''

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

        '''
        generates a volume dictionary for the valve controller based on an input ingredient
        :param ingredient: ingredient key from the library
        :param library: library with all loaded ingredients
        :return: dictionary with valve position and volume to dispense [Int:Float]
        '''

        hardware.Display.write_display(["adding:", ingredient])

        valve_volume_dict = dict()
        valves = library.ingredients_dict[ingredient]
        valve_volume_dict[valves[self.ingredient_key_alternator[ingredient]]] = mixing_by_ingredients_volume
        self.ingredient_key_alternator[ingredient] += 1
        if self.ingredient_key_alternator[ingredient] == self.ingredient_key_size[ingredient]:
            self.ingredient_key_alternator[ingredient] = 0

        return valve_volume_dict

    @staticmethod
    def chose_recipe(dice_roll_number, library):

        '''
        chose a recipe based on an integer number
        :param dice_roll_number: integer that represent a dice roll
        :param library: library with all recipes
        :return: recipe position as int
        '''

        float_ = (float(dice_roll_number) / float((Dice.dice_possible_outcomes + 1))) * len(library.recipes_list)
        return int(float_)

    @staticmethod
    def chose_ingredient(dice_roll_number, library):

        '''
        chose an ingredient based on an integer number
        :param dice_roll_number: integer that represent a dice roll
        :param library: library with all ingredients
        :return: ingredient position as int
        '''

        float_ = (float(dice_roll_number) / float((Dice.dice_possible_outcomes + 1))) * len(library.ingredients_dict)
        return int(float_)


mixing_by_ingredients_volume = 50   # ml
