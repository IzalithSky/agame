from cell import Cell
from behaviour_simple import Behaviour
from unit import Unit


class Game:
    cells: dict  # {str, Cell}
    units: dict  # {str, Unit}

    def __init__(self):
        self.cells = {}
        self.units = {}

        cell_index = 0
        cell0: Cell = Cell(uid=cell_index, x=0, y=0, food_production=.1, comfort=.1)
        self.cells[cell_index] = cell0

        unit_index = 0
        behaviour_basic: Behaviour = Behaviour(
            food_decay_rate=.05,
            food_acceptable=.3, rest_acceptable=.3,
            food_comfortable=.6, rest_comfortable=.6,
            mood_change_rate_food_base=.01, mood_change_rate_rest_base=.01)
        unit0: Unit = Unit(uid=unit_index,
                           food_prod_mult=1, good_to_bad_perception_ratio=1 / 3,
                           cell=cell0, behaviour=behaviour_basic)
        self.units[unit_index] = unit0

    def tick(self):
        for index, unit in self.units.items():
            unit.tick()

    def draw(self):
        print('cells')
        for index, cell in self.cells.items():
            print('\tuid: ', cell.uid,
                  '\tx: ', cell.x, '\ty: ', cell.y,
                  '\tfood_production: ', cell.food_production,
                  '\tcomfort: ', cell.comfort)

        print('units')
        for index, unit in self.units.items():
            print('\tuid: ', unit.uid,
                  '\tis alive: ', unit.is_alive(),
                  '\tfood: ', unit.food,
                  '\trest: ', unit.rest,
                  '\tmood: ', unit.mood,
                  '\tstate: ', unit.b_mode)
