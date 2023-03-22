import random

class Fruit:
    def __init__(self, sprite_size, field, img):
        self.sprite = img
        self.sprite_size = sprite_size

        self.position = (field[0] - 1, field[1] - 1)
        self.field = field

    def move(self, forbidden_positions):
        while True:
            self.position = (random.randint(0, self.field[0] - 1), random.randint(0, self.field[0] - 1))
            if self.position not in forbidden_positions:
                break