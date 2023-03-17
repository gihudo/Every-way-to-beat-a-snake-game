import pygame
from pygame.locals import *

class Snake:
    def __init__(self, screen):
        self.screen = screen

        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = 0
        self.y = 0
        self.speed = 10
    
    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

class Game:
    def __init__(self, size, color):
        self.color = color
        self.size = size

        pygame.init()
        self.surface = pygame.display.set_mode(size)
        self.snake = Snake(self.surface)

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
            
            self.__draw()
            

    def __draw(self):
        self.surface.fill(self.color)
        self.surface.blit(self.snake.block, (self.snake.x, self.snake.y))
        pygame.display.update()


if __name__ == "__main__":
    game = Game((500, 500), (155, 155, 155))
    game.run()