import pygame
from pygame.locals import *

class Apple:
    def __init__(self, block_size):
        self.block = pygame.image.load("resources/apple.png").convert_alpha()
        self.block = pygame.transform.scale(self.block, (block_size, block_size))

        self.pos = (0, 0)

class Snake:
    def __init__(self, block_size, length=2):
        self.block = pygame.image.load("resources/block.png").convert_alpha()
        self.block = pygame.transform.scale(self.block, (block_size, block_size))

        self.size = self.block.get_size()[0]
        self.speed = self.size

        self.length = length
        self.blocks_pos = [[0, 0]] * length

        self.direction = "right"
        self.directions_dict = {
            "right": (self.speed, 0),
            "left": (-self.speed, 0),
            "up": (0, -self.speed),
            "down": (0, self.speed)
        }

    def change_direction_left(self):
        if self.direction != "right":
            self.direction = "left"

    def change_direction_right(self):
        if self.direction != "left":
            self.direction = "right"

    def change_direction_up(self):
        if self.direction != "down":
            self.direction = "up"

    def change_direction_down(self):
        if self.direction != "up":
            self.direction = "down"

    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.blocks_pos[i] = self.blocks_pos[i - 1].copy()
        self.blocks_pos[0] = [x + y for x, y in zip(self.blocks_pos[0], self.directions_dict[self.direction])]

class Game:
    def __init__(self, field, cell_size, color):
        self.color = color
        self.field = field
        self.block_size = cell_size

        pygame.init()
        self.surface = pygame.display.set_mode(tuple(x * cell_size for x in field))

        self.snake = Snake(cell_size, 5)
        self.apple = Apple(cell_size)

        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.snake.change_direction_right()
                    elif event.key == K_LEFT:
                        self.snake.change_direction_left()
                    elif event.key == K_UP:
                        self.snake.change_direction_up()
                    elif event.key == K_DOWN:
                        self.snake.change_direction_down()
                elif event.type == QUIT:
                    running = False
            
            self.snake.move()
            self.__draw()
            self.clock.tick(5)

    def __draw(self):
        self.surface.fill(self.color)

        for i in range(self.snake.length):
            self.surface.blit(self.snake.block, self.snake.blocks_pos[i])
        self.surface.blit(self.apple.block, self.apple.pos)

        pygame.display.update()

if __name__ == "__main__":
    game = Game(field = (10, 10), cell_size = 50, color = (0, 0, 0))
    game.run()