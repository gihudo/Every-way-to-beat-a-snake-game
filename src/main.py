import pygame, sys
import random
from pygame.locals import *

class Apple:
    def __init__(self, block_size, field):
        self.block = pygame.image.load("resources/apple.png").convert_alpha()
        self.block = pygame.transform.scale(self.block, (block_size, block_size))

        self.pos = (0, 0)
        self.field = field

    def move(self, snake_body):
        while True:
            self.pos = (random.randint(0, self.field[0] - 1), random.randint(0, self.field[0] - 1))
            print(snake_body, self.pos)
            if self.pos not in snake_body:
                break

class Snake:
    def __init__(self, block_size, field, length=2):
        self.block = pygame.image.load("resources/block.png").convert_alpha()
        self.block = pygame.transform.scale(self.block, (block_size, block_size))

        self.size = self.block.get_size()[0]
        self.speed = self.size

        self.length = length
        self.blocks_pos = [(0, 0)] * length

        self.direction = "right"
        self.previous_direction = self.direction
        self.directions_dict = {
            "right": (1, 0),
            "left": (-1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }

        self.field = field

    def is_apple_collision(self, apple):
        if tuple(self.blocks_pos[0]) == apple.pos:
            self.length += 1
            self.blocks_pos.append(self.blocks_pos[-1])
            apple.move(self.blocks_pos)


    def is_body_collision(self):
        for pos in self.blocks_pos[1:]:
            if self.blocks_pos[0] == pos:
                print("COLLIDED")

    def change_direction_left(self):
        if self.previous_direction != "right":
            self.direction = "left"

    def change_direction_right(self):
        if self.previous_direction != "left":
            self.direction = "right"

    def change_direction_up(self):
        if self.previous_direction != "down":
            self.direction = "up"

    def change_direction_down(self):
        if self.previous_direction != "up":
            self.direction = "down"

    def move(self):
        self.previous_direction = self.direction

        for i in range(self.length - 1, 0, -1):
            self.blocks_pos[i] = self.blocks_pos[i - 1]
        self.blocks_pos[0] = tuple(x + y for x, y in zip(self.blocks_pos[0], self.directions_dict[self.direction]))
        self.blocks_pos[0] = tuple(x % y for x, y in zip(self.blocks_pos[0], self.field))

class Game:
    def __init__(self, field=(15,15), block_size=50, color=(0,0,0), difficulty=8):
        self.color = color
        self.field = field
        self.block_size = block_size
        self.difficulty = difficulty

        pygame.init()
        self.surface = pygame.display.set_mode(tuple(x * block_size for x in field))

        self.snake = Snake(block_size, self.field)
        self.apple = Apple(block_size, self.field)

        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        while True:
            self.__key_events()
            self.snake.move()
            self.snake.is_apple_collision(self.apple)
            self.__draw()
            self.clock.tick(self.difficulty)

    def __key_events(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.snake.change_direction_right()
                    elif event.key == K_LEFT:
                        self.snake.change_direction_left()
                    elif event.key == K_UP:
                        self.snake.change_direction_up()
                    elif event.key == K_DOWN:
                        self.snake.change_direction_down()

    def __draw(self):
        self.surface.fill(self.color)

        for i in range(self.snake.length):
            self.surface.blit(self.snake.block, tuple(coordinates * self.block_size for coordinates in self.snake.blocks_pos[i]))
        self.surface.blit(self.apple.block, tuple(coordinates * self.block_size for coordinates in self.apple.pos))

        pygame.display.update()

if __name__ == "__main__":
    game = Game(field=(5,5),block_size=100,difficulty=5)
    game.run()