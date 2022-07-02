class Cell:
    uid: str
    x: int
    y: int
    food_production: float
    comfort: float

    def __init__(self, uid,
                 x: int,
                 y: int,
                 food_production: float,
                 comfort: float):
        self.uid = uid
        self.x = x
        self.y = y
        self.food_production = food_production
        self.comfort = comfort
