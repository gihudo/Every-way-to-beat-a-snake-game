import pygame
from pygame.locals import *

class Snake:
    def __init__(self, screen, length):
        self.screen = screen

        self.block = pygame.image.load("resources/block.jpg").convert()
        self.size = self.block.get_size()[0]
        self.length = length

        self.blocks_pos = [[self.size, self.size]] * length

        self.direction = "right"
    
    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.blocks_pos[i] = self.blocks_pos[i - 1].copy()

        if self.direction == "right":
            self.blocks_pos[0][0] += self.size
        elif self.direction == "left":
            self.blocks_pos[0][0] -= self.size
        elif self.direction == "up":
            self.blocks_pos[0][1] -= self.size
        elif self.direction == "down":
            self.blocks_pos[0][1] += self.size

class Game:
    def __init__(self, size, color):
        self.color = color
        self.size = size

        pygame.init()
        self.surface = pygame.display.set_mode(size)
        self.snake = Snake(self.surface, 5)
        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                elif event.type == QUIT:
                    running = False
            
            self.snake.walk()
            self.__draw()
            self.clock.tick(5)

    def __draw(self):
        self.surface.fill(self.color)
        for i in range(self.snake.length):
            self.surface.blit(self.snake.block, tuple(self.snake.blocks_pos[i]))
        pygame.display.update()

if __name__ == "__main__":
    game = Game((500, 500), (155, 155, 155))
    game.run()