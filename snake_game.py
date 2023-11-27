import random
import curses

# define constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

MOVE_MAP = {
    UP: [0, -1],
    DOWN: [0, 1],
    LEFT: [-1, 0],
    RIGHT: [1, 0]
}

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height = 20
        self.width = 40
        self.win = curses.newwin(self.height, self.width, 0, 0)
        self.win.keypad(1)
        self.win.timeout(100)

        self.init_game()

    def init_game(self):
        self.snake = [[10, 10], [11, 10], [12, 10]]
        self.food = [20, 20]
        self.score = 0
        self.direction = RIGHT

    def get_next_position(self):
        dx, dy = MOVE_MAP[self.direction]
        next_x = self.snake[-1][0] + dx
        next_y = self.snake[-1][1] + dy

        return [next_x, next_y]

    def move_snake(self):
        next_position = self.get_next_position()

        # check collision with boundaries
        if (
            next_position[0] < 0 or next_position[0] >= self.width or
            next_position[1] < 0 or next_position[1] >= self.height
        ):
            self.init_game()
            return False

        # check collision with self
        if next_position in self.snake:
            self.init_game()
            return False

        self.snake.append(next_position)

        # check if the snake has eaten the food
        if next_position == self.food:
            self.score += 1
            self.food = None
            while self.food is None:
                nx = random.randint(0, self.width - 1)
                ny = random.randint(0, self.height - 1)
                if [nx, ny] not in self.snake:
                    self.food = [nx, ny]
        else:
            self.snake.pop(0)

        return True

    def play(self):
        while True:
            self.win.border(0)
            self.win.timeout(100)

            self.win.addch(self.food[1], self.food[0], curses.ACS_PI)

            for i in range(len(self.snake)):
                self.win.addch(self.snake[i][1], self.snake[i][0], '#' if i == 0 else '*')

            self.win.addstr(0, 2, f"Score: {self.score}")
            self.win.refresh()

            key = self.win.getch()

            if key == curses.KEY_DOWN and self.direction != UP:
                self.direction = DOWN
            elif key == curses.KEY_UP and self.direction != DOWN:
                self.direction = UP
            elif key == curses.KEY_LEFT and self.direction != RIGHT:
                self.direction = LEFT
            elif key == curses.KEY_RIGHT and self.direction != LEFT:
                self.direction = RIGHT
            elif key == curses.KEY_EXIT or key == ord('q'):
                break

            if not self.move_snake():
                break

def main():
    curses.wrapper(SnakeGame)

if __name__ == "__main__":
    main()