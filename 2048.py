import random
import pygame
import sys
import math


def message(size, word, color):
    set_font = pygame.font.SysFont("Courier New", size, True)
    set_color = set_font.render(word, True, color)
    get_dimension = set_color.get_rect()
    return set_color, get_dimension[2], get_dimension[3]


def new_block():
    return random.randint(1, 2) * 2


def new_block_location(location, new):
    spaces = 0
    for i in range(ROWS):
        spaces += location[i].count(' ')
    new_space = random.randint(1, spaces)
    found_space = 0
    for r in range(ROWS):
        for c in range(COLUMNS):
            if location[r][c] == ' ':
                found_space += 1
            if found_space == new_space:
                location[r][c] = new
                return location


def up_slide(location, points, slide):
    x = 0
    while x < COLUMNS:
        y = ROWS - 1
        space = 0
        while y >= 0:
            if location[x][y] == ' ':
                space += 1
            elif space > 0:
                location[x][y + space] = location[x][y]
                location[x][y] = ' '
                y += space
                space = 0
                slide = True
            y -= 1
        x += 1
    x = 0
    while x < COLUMNS:
        y = ROWS - 1
        step = []
        while y > 0:
            if location[x][y] == location[x][y - 1] and location[x][y] != ' ':
                location[x][y] *= 2
                points += location[x][y]
                step.append(y)
                y -= 1
                slide = True
            y -= 1
        if len(step) > 1:
            location[x][2] = location[x][1]
            location[x][1] = ' '
            location[x][0] = ' '
        elif 3 in step:
            location[x][2] = location[x][1]
            location[x][1] = location[x][0]
            location[x][0] = ' '
        elif 2 in step:
            location[x][1] = location[x][0]
            location[x][0] = ' '
        elif 1 in step:
            location[x][0] = ' '
        x += 1
    return location, points, slide


def down_slide(location, points, slide):
    x = 0
    while x < 4:
        y = 0
        space = 0
        while y <= 3:
            if location[x][y] == ' ':
                space += 1
            elif space > 0:
                location[x][y - space] = location[x][y]
                location[x][y] = ' '
                y -= space
                space = 0
                slide = True
            y += 1
        x += 1
    x = 0
    while x < 4:
        y = 0
        step = []
        while y < 3:
            if location[x][y] == location[x][y + 1] and location[x][y] != ' ':
                location[x][y] *= 2
                points += location[x][y]
                step.append(y)
                y += 1
                slide = True
            y += 1
        if len(step) > 1:
            location[x][1] = location[x][2]
            location[x][2] = ' '
            location[x][3] = ' '
        elif 0 in step:
            location[x][1] = location[x][2]
            location[x][2] = location[x][3]
            location[x][3] = ' '
        elif 1 in step:
            location[x][2] = location[x][3]
            location[x][3] = ' '
        elif 2 in step:
            location[x][3] = ' '
        x += 1
    return location, points, slide


def left_slide(location, points, slide):
    y = 0
    while y < 4:
        x = 0
        space = 0
        while x <= 3:
            if location[x][y] == ' ':
                space += 1
            elif space > 0:
                location[x - space][y] = location[x][y]
                location[x][y] = ' '
                x -= space
                space = 0
                slide = True
            x += 1
        y += 1
    y = 0
    while y < 4:
        x = 0
        step = []
        while x < 3:
            if location[x][y] == location[x + 1][y] and location[x][y] != ' ':
                location[x][y] *= 2
                points += location[x][y]
                step.append(x)
                x += 1
                slide = True
            x += 1
        if len(step) > 1:
            location[1][y] = location[2][y]
            location[2][y] = ' '
            location[3][y] = ' '
        elif 0 in step:
            location[1][y] = location[2][y]
            location[2][y] = location[3][y]
            location[3][y] = ' '
        elif 1 in step:
            location[2][y] = location[3][y]
            location[3][y] = ' '
        elif 2 in step:
            location[3][y] = ' '
        y += 1
    return location, points, slide


def right_slide(location, points, slide):
    y = 0
    while y < 4:
        x = 3
        space = 0
        while x >= 0:
            if location[x][y] == ' ':
                space += 1
            elif space > 0:
                location[x + space][y] = location[x][y]
                location[x][y] = ' '
                x += space
                space = 0
                slide = True
            x -= 1
        y += 1
    y = 0
    while y < 4:
        x = 3
        step = []
        while x > 0:
            if location[x][y] == location[x - 1][y] and location[x][y] != ' ':
                location[x][y] *= 2
                points += location[x][y]
                step.append(x)
                x -= 1
                slide = True
            x -= 1
        if len(step) > 1:
            location[2][y] = location[1][y]
            location[1][y] = ' '
            location[0][y] = ' '
        elif 3 in step:
            location[2][y] = location[1][y]
            location[1][y] = location[0][y]
            location[0][y] = ' '
        elif 2 in step:
            location[1][y] = location[0][y]
            location[0][y] = ' '
        elif 1 in step:
            location[0][y] = ' '
        y += 1
    return location, points, slide


def draw_board(location, points):
    pygame.draw.rect(screen, RED, (0, 0, SQUARESIZE * COLUMNS, SQUARESIZE))

    text, head_x2, head_y2 = message(88, str(points), BLACK)
    headx = (SQUARESIZE * COLUMNS - head_x2) / 2
    heady = (SQUARESIZE - head_y2) / 2

    screen.blit(text, (headx, heady, SQUARESIZE * COLUMNS, SQUARESIZE))

    for c in range(COLUMNS):
        for r in range(ROWS):
            if location[r][c] != ' ':
                tile_color = 255 - (math.log(location[r][c], 2) * 11)
                pygame.draw.rect(screen, (tile_color, tile_color, tile_color), (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))

                values_size = 72 - (len(str(location[r][c])) * 8)
                text, x2, y2 = message(values_size, str(location[r][c]), RED)
                x = (SQUARESIZE - x2) / 2
                y = (SQUARESIZE - y2) / 2

                screen.blit(text, (c * SQUARESIZE + x, r * SQUARESIZE + SQUARESIZE + y, SQUARESIZE, SQUARESIZE))
            else:
                pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
    pygame.display.update()


def check_end(location):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if location[r][c] == ' ':
                return False
            elif r == 3 and c == 3:
                return True
            elif r == 3:
                if location[r][c] == location[r][c + 1]:
                    return False
            elif c == 3:
                if location[r][c] == location[r + 1][c]:
                    return False
            elif location[r][c] == location[r + 1][c] or location[r][c] == location[r][c + 1]:
                return False


def game_over():
    pygame.time.wait(1000)
    pygame.draw.rect(screen, GRAY, (50, 150, 300, 200))
    pygame.draw.rect(screen, RED, (50, 250, 150, 100))
    pygame.draw.rect(screen, GREEN, (200, 250, 150, 100))

    text, x2, y2 = message(22, "GAME OVER. PLAY AGAIN?", BLACK)
    x = (300 - x2) / 2
    y = (100 - y2) / 2
    screen.blit(text, (50 + x, 150 + y, 300 - x, 100 - y))

    text, x2, y2 = message(32, "NO", BLACK)
    x = (150 - x2) / 2
    y = (100 - y2) / 2
    screen.blit(text, (50 + x, 250 + y, 150 - x, 100 - y))

    text, x2, y2 = message(32, "YES", BLACK)
    x = (150 - x2) / 2
    y = (100 - y2) / 2
    screen.blit(text, (200 + x, 250 + y, 150 - x, 100 - y))

    pygame.display.update()

    repeat = None
    while True:
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                sys.exit()
            if event2.type == pygame.MOUSEBUTTONDOWN:
                posx = event2.pos[0]
                posy = event2.pos[1]
                if 200 <= posx <= 350 and 250 <= posy <= 350:
                    repeat = True
                elif 50 <= posx <= 200 and 250 <= posy <= 350:
                    repeat = False
        if repeat is not None:
            break

    return repeat


def start_game():
    location = [[' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ']]
    points = 0
    slide = True
    new_block_location(location, new_block())
    new_block_location(location, new_block())
    
    return location, points, slide


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (80, 80, 80)
SQUARESIZE = 100
ROWS = 4
COLUMNS = 4

pygame.init()

size = (COLUMNS * SQUARESIZE, (ROWS + 1) * SQUARESIZE)
screen = pygame.display.set_mode(size)

grid, score, moved = start_game()

draw_board(grid, score)

play_again = True
while play_again:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                grid, score, moved = up_slide(grid, score, False)
            if event.key == pygame.K_LEFT:
                grid, score, moved = down_slide(grid, score, False)
            if event.key == pygame.K_UP:
                grid, score, moved = left_slide(grid, score, False)
            if event.key == pygame.K_DOWN:
                grid, score, moved = right_slide(grid, score, False)
            if moved:
                new_block_location(grid, new_block())
            draw_board(grid, score)
            if check_end(grid):
                play_again = game_over()
                if play_again:
                    grid, score, moved = start_game()
                    draw_board(grid, score)
