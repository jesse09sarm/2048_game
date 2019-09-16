import random
import pygame
import math
import sys

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (80, 80, 80)

# screen
SQUARESIZE = 100
ROWS = 4
COLUMNS = 4

pygame.init()

# creates game display
size = (COLUMNS * SQUARESIZE, (ROWS + 1) * SQUARESIZE)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("2048 Game")



# takes size, text, color of new message to be displayed
# returns configured text block and width,height dimensions
# dimensions so text block can be centered in desired location of the screen
def message(size, word, color):
    # sets font with hard coded font type and passed in size 
    set_font = pygame.font.SysFont("Courier New", size, True)

    # creates text block with passed in message and color
    set_color = set_font.render(word, True, color)

    # gets dimension of text block in form [left,top,width,height]
    get_dimension = set_color.get_rect()

    return set_color, get_dimension[2], get_dimension[3]


# returns the value of the new block to be added to the grid
# randomly returns a 2 or 4
def new_block():
    return random.randint(1, 2) * 2


# finds available spaces for new value
# adds randomly created value to random spot on the grid
def new_block_location(location, new):
    # amount of empty spaces
    spaces = 0

    # finds empty spaces in the grid
    for i in range(ROWS):
        spaces += location[i].count(' ')

    # picks one of the random spaces
    new_space = random.randint(1, spaces)

    # variable holds amount of spaces gone over
    # to select a specific one new_space
    found_space = 0


    for r in range(ROWS):
        for c in range(COLUMNS):
            if location[r][c] == ' ':
                found_space += 1

            # inserts the random value at the random empty space
            if found_space == new_space:
                location[r][c] = new
                return location


def up_slide(location, points):
    slide = False
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


def down_slide(location, points):
    slide = False
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


def left_slide(location, points):
    slide = False
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


def right_slide(location, points):
    slide = False
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


# draws the game board
# takes in location and points to update grid and score
def draw_board(location, points):
    # red header rectangle
    pygame.draw.rect(screen, RED, (0, 0, SQUARESIZE * COLUMNS, SQUARESIZE))

    # creates text block of the score
    text, head_x2, head_y2 = message(88, str(points), BLACK)

    # variables help find center of header to place score
    headx = (SQUARESIZE * COLUMNS - head_x2) / 2
    heady = (SQUARESIZE - head_y2) / 2

    # places the score total on the header rectangle
    screen.blit(text, (headx, heady, SQUARESIZE * COLUMNS, SQUARESIZE))

    # iterates through grid to display each tile 
    # tiles has specific colors and font sizes 
    for c in range(COLUMNS):
        for r in range(ROWS):

            # this is a tile with a value
            if location[r][c] != ' ':

                # tile colors get darker in grayscale when increasing 
                tile_color = 255 - (math.log(location[r][c], 2) * 11)

                # colors the tile
                pygame.draw.rect(screen, (tile_color, tile_color, tile_color), (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))

                # font size of tiles have to decrease as it increases to fit in tiles
                values_size = 72 - (len(str(location[r][c])) * 8)

                # creates text block of value on tile
                text, x2, y2 = message(values_size, str(location[r][c]), RED)

                # centers value on tile
                x = (SQUARESIZE - x2) / 2
                y = (SQUARESIZE - y2) / 2

                # places text value on the tile 
                screen.blit(text, (c * SQUARESIZE + x, r * SQUARESIZE + SQUARESIZE + y, SQUARESIZE, SQUARESIZE))
            
            # this is an empty space
            else:
                # empty space is colored black
                pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
    
    # simply updates game display
    pygame.display.update()


# checks if there are any valid swipes left
def check_end(location):
    # iterates through the grid
    for r in range(ROWS):
        for c in range(COLUMNS):

            # an empty space means there is always a valid swipe remaining 
            if location[r][c] == ' ':
                return False

            # if the check gets to the last row and column 
            # means it did not found a valid swipe throughout the grid
            elif r == 3 and c == 3:
                return True

            # once on the bottom row 
            # only checks value to the right for an equal value
            elif r == 3:
                if location[r][c] == location[r][c + 1]:
                    return False

            # once on the furthest right column
            # only checks value below for an equal value
            elif c == 3:
                if location[r][c] == location[r + 1][c]:
                    return False

            # checks value to the right and below for an equal value
            # if equal value then a swipe in that direction is valid to combine the values
            elif location[r][c] == location[r + 1][c] or location[r][c] == location[r][c + 1]:
                return False


# runs at the end of game
# asks user to play again
def game_over():
    # gives user 1 second to end game of the board
    pygame.time.wait(1000)

    # draws rectangles to place game over message
    pygame.draw.rect(screen, GRAY, (50, 150, 300, 200))
    pygame.draw.rect(screen, RED, (50, 250, 150, 100))
    pygame.draw.rect(screen, GREEN, (200, 250, 150, 100))

    # creates game over text block
    text, x2, y2 = message(22, "GAME OVER. PLAY AGAIN?", BLACK)

    # centers text block
    x = (300 - x2) / 2
    y = (100 - y2) / 2

    # places text block on the game display
    screen.blit(text, (50 + x, 150 + y, 300 - x, 100 - y))

    # creates choice of NO text block
    text, x2, y2 = message(32, "NO", BLACK)

    # centers text block
    x = (150 - x2) / 2
    y = (100 - y2) / 2

    # places text block on its red rectangle on game display
    screen.blit(text, (50 + x, 250 + y, 150 - x, 100 - y))

    # creates choice of YES text block
    text, x2, y2 = message(32, "YES", BLACK)

    # centers text block
    x = (150 - x2) / 2
    y = (100 - y2) / 2

    # places text block on its green rectangle on game display
    screen.blit(text, (200 + x, 250 + y, 150 - x, 100 - y))

    # simply updates game display
    pygame.display.update()

    # repeat will hold the users answer to play again
    repeat = None

    # gets users input until chooses an option or exits the window
    while True:

        # gets users inputs
        for event2 in pygame.event.get():

            # user exits window code terminates
            if event2.type == pygame.QUIT:
                sys.exit()

            # user clicks somewhere on the display
            if event2.type == pygame.MOUSEBUTTONDOWN:

                # position of the mouse click in pixels
                posx = event2.pos[0]
                posy = event2.pos[1]

                # checks if x,y is within the YES block
                if 200 <= posx <= 350 and 250 <= posy <= 350:
                    repeat = True

                # checks if x,y is within the NO block
                elif 50 <= posx <= 200 and 250 <= posy <= 350:
                    repeat = False

        # breaks loop when user has chosen an option
        if repeat is not None:
            break

    return repeat


# sets variables for start of game
# sets grid, score, and moved
def start_game():
    # grid of values represents the tiles on the board
    location = [[' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ']]

    # starting score
    points = 0

    # whether an intended slide actually moved a tile
    slide = True
    
    # places random starting tiles on random places of the board
    new_block_location(location, new_block())
    new_block_location(location, new_block())
    
    return location, points, slide