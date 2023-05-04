import sys
sys.path.append('D:\GitHub\Snake-pygame\src\snake_game')

import snake, fruit

import pygame
from pygame.locals import *

class Game:
    def __init__(self, field=(15,15), block_size=50, color=(0,0,0), difficulty=8):
        self.field = field
        self.block_size = block_size
        self.bg_color = color
        self.difficulty = difficulty
        
        self.running = True
        self.score = 2
        self.n_games = 0
        self.max_score = (field[0] - 1) * (field[1] - 1)

        pygame.init()
        self.surface = pygame.display.set_mode(tuple(x * block_size for x in field))
        pygame.display.set_caption(f"Snake: {self.score}")
        self.__load_resources()

        self.fruit = fruit.Fruit(
            sprite_size = block_size,
            field = self.field,
            img = self.fruit_sprite
            )

        self.snake = snake.Snake(
            sprite_size = self.block_size, 
            field = self.field,
            img = self.snake_body_sprite
            )

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 30)

    def next(self):
        if self.running:
            self.snake.move()

            self.__handle_keyboard_events()
            self.__handle_collisions()
            self.__update_screen()

            self.clock.tick(self.difficulty)

    def __handle_collisions(self):
        if self.snake.is_body_collision():
            self.__game_over()

        if self.snake.is_collision(self.fruit.position):
            self.fruit.move(self.snake.positions)
            self.snake.add_length()
            self.score += 1

            if self.snake.length == self.max_score:
                self.__game_win()
                
            pygame.display.set_caption(f"Snake: {self.score}")

    def __game_over(self):
        self.running = False

    def __game_win(self):
        pass

    def reset(self):
        self.running = True
        self.score = 2
        self.n_games += 1
        self.snake.length = 2
        self.snake.positions = [(0, 0)] * 2

        self.fruit.position = (self.field[0] - 1, self.field[1] - 1)


    def __handle_keyboard_events(self):
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
                    elif event.key == K_1:
                        self.difficulty -= 10
                    elif event.key == K_2:
                        self.difficulty += 10


    def __update_screen(self):
        self.surface.fill(self.bg_color)

        for i in range(self.snake.length):
            self.surface.blit(self.snake.sprite, tuple(coordinates * self.block_size for coordinates in self.snake.positions[i]))
        self.surface.blit(self.fruit.sprite, tuple(coordinates * self.block_size for coordinates in self.fruit.position))

        pygame.display.update()
    
    def __load_resources(self):
        self.fruit_sprite = pygame.transform.scale(pygame.image.load("resources/fruit.png").convert_alpha(), (self.block_size, self.block_size))
        self.snake_body_sprite = pygame.transform.scale(pygame.image.load("resources/snake_body.png").convert_alpha(), (self.block_size, self.block_size))
