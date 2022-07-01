class Unit:
    uid: str
    food: float
    rest: float
    mood: float

    def __init__(self, uid):
        self.uid = uid
        self.food = .5
        self.rest = 1
        self.mood = .5

    def is_alive(self) -> bool:
        return self.food > 0


