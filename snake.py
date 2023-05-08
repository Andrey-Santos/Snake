import random
import curses

height, width = curses.initscr().getmaxyx()
window = curses.newwin(height, width, 0, 0)
snake = [[2, 4], [2, 3], [2, 2]]
head_position = [2, 4]
apple = [5, 5]

# Initial values for the game
key = -1
new_key = curses.KEY_RIGHT
last_direction = 'r'
score = 0
movement_speed = 100


def main():
    curses.curs_set(False)
    window.keypad(True)
    window.nodelay(True)
    start_game()
    window.addstr(int(height / 2), int(width / 2.5), "Score: " + str(score))
    window.refresh()
    curses.napms(2000)
    curses.endwin()


def start_game():
    create_scenario()
    while True:
        control_snake_movement()

        if verify_collision() == -1 or snake[0] in snake[1:]:
            break

        snake.insert(0, list(head_position))
        window.addch(head_position[0], head_position[1], '#')

        curses.napms(movement_speed)
        window.refresh()


def create_scenario():
    # create top and bottom borders
    for pos in range(0, width - 1):
        window.addch(0, pos, '#')
        window.addch(height - 1, pos, '#')

    # creates side borders
    for pos in range(0, height - 1):
        window.addch(pos, 0, '#')
        window.addch(pos, width - 1, '#')

    # create the snake
    for pos in range(0, len(snake)):
        window.addch(snake[pos][0], snake[pos][1], '#')

    # create the first apple
    create_new_apple()


def create_new_apple():
    global apple
    apple = [random.randint(1, height - 2), random.randint(1, width - 2)]
    window.addch(apple[0], apple[1], '*')


def control_snake_movement():
    global new_key, key, last_direction
    new_key = window.getch()
    key = key if new_key == -1 else new_key

    if key == curses.KEY_DOWN and last_direction != 'u':
        last_direction = 'd'
    elif key == curses.KEY_UP and last_direction != 'd':
        last_direction = 'u'
    elif key == curses.KEY_LEFT and last_direction != 'r':
        last_direction = 'l'
    elif key == curses.KEY_RIGHT and last_direction != 'l':
        last_direction = 'r'

    if last_direction == 'r':
        head_position[1] += 1
    elif last_direction == 'l':
        head_position[1] -= 1
    elif last_direction == 'u':
        head_position[0] -= 1
    elif last_direction == 'd':
        head_position[0] += 1


def verify_collision():




    global apple, score, movement_speed

    if head_position == apple:
        score += 1
        create_new_apple()
        movement_speed = movement_speed - 10 if movement_speed - 10 > 5 else movement_speed
    elif (head_position[0] == height - 1 or head_position[0] == 0) or (
            head_position[1] == width - 1 or head_position[1] == 0):
        return -1
    else:
        tail = snake.pop()
        window.addch(tail[0], tail[1], ' ')

    return 1


if __name__ == "__main__":
    main()
