from enum import Enum

class Snake:

    class Directions(Enum):
        RIGHT = (1, 0)
        LEFT = (-1, 0)
        UP = (0, -1)
        DOWN = (0, 1)

    def __init__(self, sprite_size, field, img, length=2):
        self.field = field
        self.sprite = img

        self.length = length
        self.positions = [(0, 0)] * length
        self.sprite_size = sprite_size

        self.speed = self.sprite_size
        self.direction = Snake.Directions.RIGHT
        self.previous_direction = self.direction

    def add_length(self):
        self.length += 1
        self.positions.append(self.positions[-1])

    def is_collision(self, pos):
        return tuple(self.positions[0]) == pos

    def is_body_collision(self, point = None):
        if point is None:
            point = self.positions[0]
        
        for position in self.positions[1:]:
            if point == position:
                return True
        return False

    def change_direction_left(self):
        if self.previous_direction != Snake.Directions.RIGHT:
            self.direction = Snake.Directions.LEFT

    def change_direction_right(self):
        if self.previous_direction != Snake.Directions.LEFT:
            self.direction = Snake.Directions.RIGHT

    def change_direction_up(self):
        if self.previous_direction != Snake.Directions.DOWN:
            self.direction = Snake.Directions.UP

    def change_direction_down(self):
        if self.previous_direction != Snake.Directions.UP:
            self.direction = Snake.Directions.DOWN

    def move(self):
        self.previous_direction = self.direction

        for i in range(self.length - 1, 0, -1):
            self.positions[i] = self.positions[i - 1]
            
        self.positions[0] = tuple(x + y for x, y in zip(self.positions[0], self.direction.value))
        self.positions[0] = tuple(x % y for x, y in zip(self.positions[0], self.field))