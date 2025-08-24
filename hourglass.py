#I like hourglasses
#so thus, this project

#needed libraries
# pip install bext (not for modern Python/other terminals)
import random, sys, time, os

# Constants
PAUSE_LENGTH = 0.03
SCREEN_WIDTH = 79
SCREEN_HEIGHT = 25
X, Y = 0, 1
SAND = '█'
TRAIL = '░'
WALL = '█'


# Walls of hourglass
HOURGLASS = set()
for i in range(18, 37):
    HOURGLASS.add((i, 1))
    HOURGLASS.add((i, 23))
for i in range(1, 5):
    HOURGLASS.add((18, i))
    HOURGLASS.add((36, i))
    HOURGLASS.add((18, i + 19))
    HOURGLASS.add((36, i + 19))
for i in range(8):
    HOURGLASS.add((19 + i, 5 + i))
    HOURGLASS.add((35 - i, 5 + i))
    HOURGLASS.add((25 - i, 13 + i))
    HOURGLASS.add((29 + i, 13 + i))

# Initial sand
INITIAL_SAND = set()
for y in range(8):
    for x in range(19 + y, 36 - y):
        INITIAL_SAND.add((x, y + 4))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def goto(x, y):
    print(f"\033[{y + 1};{x + 1}H", end='')


def set_color(color_code):
    print(f"\033[{color_code}m", end='')


def reset_color():
    print("\033[0m", end='')


def draw_hourglass():
    set_color(33)
    for wall in HOURGLASS:
        goto(wall[X], wall[Y])
        print(WALL, end='')
    reset_color()


def draw_sand(allSand):
    set_color(33)
    for sand in allSand:
        goto(sand[X], sand[Y])
        print(SAND, end='')
    reset_color()


def run_hourglass_simulation(allSand):
    trails = []

    while True:
        random.shuffle(allSand)
        moved = False

        for i, sand in enumerate(allSand):
            if sand[Y] >= SCREEN_HEIGHT - 1:
                continue

            below = (sand[X], sand[Y] + 1)
            down_left = (sand[X] - 1, sand[Y] + 1)
            down_right = (sand[X] + 1, sand[Y] + 1)

            # Try falling down
            if below not in allSand and below not in HOURGLASS:
                move_to = below
            elif down_left not in allSand and down_left not in HOURGLASS and (sand[X] - 1, sand[Y]) not in HOURGLASS:
                move_to = down_left
            elif down_right not in allSand and down_right not in HOURGLASS and (sand[X] + 1, sand[Y]) not in HOURGLASS:
                move_to = down_right
            else:
                move_to = None

            if move_to:
                # Draw trail
                goto(sand[X], sand[Y])
                set_color(37)
                print(TRAIL, end='')
                trails.append((sand[X], sand[Y], 3))
                reset_color()

                # Move sand
                goto(move_to[X], move_to[Y])
                set_color(33)
                print(SAND, end='')
                reset_color()
                allSand[i] = move_to
                moved = True

        # Update trails
        for t in trails[:]:
            x, y, life = t
            life -= 1
            trails.remove(t)
            if life > 0:
                trails.append((x, y, life))
                goto(x, y)
                set_color(37)
                print(TRAIL, end='')
                reset_color()
            else:
                goto(x, y)
                print(' ', end='')

        sys.stdout.flush()
        time.sleep(PAUSE_LENGTH)

        if not moved:
            time.sleep(1)
            # Clear sand only
            for sand in allSand:
                goto(sand[X], sand[Y])
                print(' ', end='')
            break


def main():
    clear_screen()
    print("Ctrl-C to quit.")
    draw_hourglass()

    while True:
        allSand = list(INITIAL_SAND)
        draw_sand(allSand)
        run_hourglass_simulation(allSand)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        sys.exit()
# End of file hourglass.py