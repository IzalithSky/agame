from enum import Enum
from cell import Cell


class BMode(Enum):
    IDLE = 0
    REST = 1
    WORK = 2


class Behaviour:
    def __init__(self):
        pass

    def tick(self, u):
        pass


class Unit:
    uid: str

    food: float
    rest: float
    mood: float

    food_prod_mult: float
    good_to_bad_perception_ratio: float

    cell: Cell
    behaviour: Behaviour
    b_mode: BMode

    def __init__(self, uid, food_prod_mult, good_to_bad_perception_ratio, behaviour, cell):
        self.uid = uid

        self.food = .5
        self.rest = 1
        self.mood = .5

        self.cell = cell

        self.food_prod_mult = food_prod_mult
        self.good_to_bad_perception_ratio = good_to_bad_perception_ratio

        self.behaviour = behaviour
        self.b_mode = None

    def is_alive(self) -> bool:
        return self.food > 0

    def tick(self):
        self.behaviour.tick(self)


class Behaviour:
    food_decay_rate: float
    food_acceptable: float
    rest_acceptable: float
    food_comfortable: float
    rest_comfortable: float
    mood_change_rate_food_base: float
    mood_change_rate_rest_base: float

    def __init__(self,
                 food_decay_rate: float,
                 food_acceptable: float,
                 rest_acceptable: float,
                 food_comfortable: float,
                 rest_comfortable: float,
                 mood_change_rate_food_base: float,
                 mood_change_rate_rest_base: float):
        self.food_decay_rate = food_decay_rate
        self.food_acceptable = food_acceptable
        self.rest_acceptable = rest_acceptable
        self.food_comfortable = food_comfortable
        self.rest_comfortable = rest_comfortable
        self.mood_change_rate_food_base = mood_change_rate_food_base
        self.mood_change_rate_rest_base = mood_change_rate_rest_base

    def is_hungry(self, u: Unit) -> bool:
        return u.food < self.food_acceptable

    def is_tired(self, u: Unit) -> bool:
        return u.rest < self.rest_acceptable

    def get_rest_regain_rate(self, u: Unit) -> float:
        rate: float = .0
        if u.cell is not None:
            rate += u.cell.comfort
        return rate

    def get_rest_decay_rate(self, u: Unit) -> float:
        rate: float = .0
        if u.cell is not None:
            if u.cell.comfort > 0:
                rate -= 1 - u.cell.comfort
            if u.cell.comfort < 0:
                rate += u.cell.comfort * u.good_to_bad_perception_ratio
        return rate

    def get_mood_change_rate_by_food(self, u: Unit) -> float:
        rate: float = .0
        if u.food < self.food_acceptable:
            rate -= self.mood_change_rate_food_base
        if u.food >= self.food_comfortable:
            rate += self.mood_change_rate_food_base * u.good_to_bad_perception_ratio
        return rate

    def get_mood_change_rate_by_rest(self, u: Unit) -> float:
        rate: float = .0
        if u.rest < self.rest_acceptable:
            rate -= self.mood_change_rate_rest_base
        if u.rest >= self.rest_comfortable:
            rate += self.mood_change_rate_rest_base
        return rate

    def decide_mode(self, u: Unit):
        if not u.is_alive():
            u.b_mode = None
            return

        if self.is_tired(u):
            u.b_mode = BMode.REST
        elif self.is_hungry(u) and not self.is_tired(u):
            u.b_mode = BMode.WORK
        else:
            u.b_mode = BMode.IDLE

    def tick_unit(self, u: Unit):
        u.food -= self.food_decay_rate

        u.mood += self.get_mood_change_rate_by_food(u)
        u.mood += self.get_mood_change_rate_by_rest(u)

        if u.mood < 0:
            u.mood = 0
        if u.mood > 1:
            u.mood = 1

    def tick_unit_rest(self, u: Unit):
        self.tick_unit(u)
        u.rest += self.get_rest_regain_rate(u)
        if u.rest < 0:
            u.rest = 0
        if u.rest > 1:
            u.rest = 1

    def tick_unit_work(self, u: Unit):
        self.tick_unit(u)
        u.rest += self.get_rest_decay_rate(u)
        if u.rest < 0:
            u.rest = 0
        if u.rest > 1:
            u.rest = 1

    def tick_unit_idle(self, u: Unit):
        self.tick_unit(u)

    def tick_cell_rest(self, u: Unit):
        return

    def tick_cell_work(self, u: Unit):
        if u.cell is not None and u.rest > 0:
            rest_prod_mult = .5 if u.rest < .5 else 1
            mood_prod_mult = .5 if u.mood < .5 else 1
            u.food += u.cell.food_production * u.food_prod_mult * rest_prod_mult * mood_prod_mult

    def tick_cell_idle(self, u: Unit):
        return

    def tick(self, u: Unit):
        self.decide_mode(u)
        match u.b_mode:
            case BMode.IDLE:
                self.tick_unit_idle(u)
                self.tick_cell_idle(u)
            case BMode.REST:
                self.tick_unit_rest(u)
                self.tick_cell_rest(u)
            case BMode.WORK:
                self.tick_unit_work(u)
                self.tick_cell_work(u)
            case _:
                return
