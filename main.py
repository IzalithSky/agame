from unit import Unit
from cell import Cell


def main():
    unit0: Unit = Unit(0)
    print(unit0, unit0.uid, unit0.food, unit0.rest, unit0.mood);
    print('is alive: ', unit0.is_alive())

    cell0: Cell = Cell(0)
    print(cell0, cell0.uid, cell0.x, cell0.y, cell0.food_production, cell0.comfort)


if __name__ == '__main__':
    main()
