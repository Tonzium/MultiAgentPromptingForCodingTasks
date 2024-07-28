import random
import time
import os

class SnakeGame:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.snake = [(0, 0)]
        self.food = None
        self.direction = 'right'
        self.score = 0

    def generate_food(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def move_snake(self):
        head = self.snake[0]
        if self.direction == 'right':
            new_head = (head[0] + 1, head[1])
        elif self.direction == 'left':
            new_head = (head[0] - 1, head[1])
        elif self.direction == 'up':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'down':
            new_head = (head[0], head[1] + 1)

        self.snake.insert(0, new_head)
        if self.snake[0] == self.food:
            self.score += 1
            self.generate_food()
        else:
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            return True
        for part in self.snake[1:]:
            if head == part:
                return True
        return False

    def play(self):
        while True:
            os.system('clear')
            print('Score:', self.score)
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) == self.food:
                        print('*', end=' ')
                    elif (x, y) in self.snake:
                        print('#', end=' ')
                    else:
                        print(' ', end=' ')
                print()
            print('Direction:', self.direction)
            user_input = input('Enter direction (w/a/s/d): ')
            if user_input == 'w' and self.direction != 'down':
                self.direction = 'up'
            elif user_input == 's' and self.direction != 'up':
                self.direction = 'down'
            elif user_input == 'a' and self.direction != 'right':
                self.direction = 'left'
            elif user_input == 'd' and self.direction != 'left':
                self.direction = 'right'
            self.move_snake()
            if self.check_collision():
                print('Game Over!')
                break
            time.sleep(0.5)

if __name__ == '__main__':
    game = SnakeGame()
    game.generate_food()
    game.play()