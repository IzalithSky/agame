class Cell:
    uid: str
    x: int
    y: int
    food_production: float
    comfort: float

    def __init__(self, uid):
        self.uid = uid
        self.x = 0
        self.y = 0
        self.food_production = 0
        self.comfort = 0

