import scripts
import hardware


class Mixer:

    def __init__(self):
        self.ingredient_key_size = dict()
        self.ingredient_key_alternator = dict()
        for key in scripts.library.ingredients_dict:
            self.ingredient_key_size[key] = len(scripts.library.ingredients_dict[key])
            self.ingredient_key_alternator[key] = 0


    def mix_drink(self, recipe):
        hardware.Display.write_display(["Mixing:", recipe.name])

        valve_volume_dict = dict()
        for ingredient in recipe.ingredients:
            condiment = ingredient[0]
            volume = ingredient[1]

            valves = scripts.library.ingredients_dict[condiment]
            valve_volume_dict[valves[self.ingredient_key_alternator[condiment]]] = volume
            self.ingredient_key_alternator[condiment] += 1
            if self.ingredient_key_alternator[condiment] == self.ingredient_key_size[condiment]:
                self.ingredient_key_alternator[condiment] = 0

        return valve_volume_dict
