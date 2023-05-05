import sys
sys.path.append('D:\GitHub\Snake-pygame\src\snake_game')

import game, snake
from model import Linear_QNet, QTrainer

from collections import deque
import numpy
import torch
import random
import time, os

MAX_MEMORY = 10_000_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen = MAX_MEMORY)

        self.model = Linear_QNet(11, 256, 4)
        if os.path.exists('model/model.pth'):
            self.model.load_state_dict(torch.load("./model/model.pth"))
            self.model.eval()
        self.trainer = QTrainer(self.model, LR, gamma=self.gamma)

    def get_state(self, game: game.Game):
        head = game.snake.positions[0]

        dir_l = game.snake.Directions.LEFT == game.snake.direction
        dir_r = game.snake.Directions.RIGHT == game.snake.direction
        dir_u = game.snake.Directions.UP == game.snake.direction
        dir_d = game.snake.Directions.DOWN == game.snake.direction

        point_l = ((head[0] - 1) % game.field[0], head[1])
        point_r = ((head[0] + 1) % game.field[0], head[1])
        point_u = (head[0], (head[1] - 1) % game.field[1])
        point_d = (head[0], (head[1] + 1) % game.field[1])

        state = [
            #forward
            (dir_r and game.snake.is_body_collision(point_r)) or
            (dir_l and game.snake.is_body_collision(point_l)) or
            (dir_u and game.snake.is_body_collision(point_u)) or
            (dir_d and game.snake.is_body_collision(point_d)),

            #right
            (dir_u and game.snake.is_body_collision(point_r)) or
            (dir_d and game.snake.is_body_collision(point_l)) or
            (dir_r and game.snake.is_body_collision(point_d)) or
            (dir_l and game.snake.is_body_collision(point_u)),

            #left
            (dir_u and game.snake.is_body_collision(point_l)) or
            (dir_d and game.snake.is_body_collision(point_r)) or
            (dir_r and game.snake.is_body_collision(point_u)) or
            (dir_l and game.snake.is_body_collision(point_d)),

            dir_r,
            dir_l,
            dir_u,
            dir_d,

            game.fruit.position[0] > head[0],
            game.fruit.position[0] < head[0],
            game.fruit.position[1] < head[1],
            game.fruit.position[1] > head[1]
        ]

        return numpy.array(state, dtype = int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        self.n_games += 1

        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        for state, action, reward, next_state, done in mini_sample:
            self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        final_move = [0, 0, 0, 0]
        #self.epsilon = 100 - self.n_games
        print(self.n_games)
        if random.randint(0, 200) < self.epsilon:
            print('random')
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def train():
        agent = Agent()
        g = game.Game(difficulty = 1)

        record = 0
        count = 0
        while True:
            state_old = agent.get_state(g)
            final_move = agent.get_action(state_old)

            if final_move == [1,0,0,0]:
                g.snake.change_direction_up()
            elif final_move == [0,1,0,0]:
                g.snake.change_direction_down()
            elif final_move == [0,0,1,0]:
                g.snake.change_direction_right()
            elif final_move == [0,0,0,1]:
                g.snake.change_direction_left()

            old_score = g.score
            g.next()

            state_new = agent.get_state(g)      
            if g.running:
                reward = 15 if old_score < g.score else 0
            else: reward = -15

            score = g.score
            done = not g.running
            print(state_new)
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            agent.remember(state_old, final_move, reward, state_new, done)
            if done:
                g.reset()
                agent.train_long_memory()

            if score > record:
                agent.model.save()
                record = score

if __name__ == '__main__':
    Agent.train()