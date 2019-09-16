from functions_2048 import *
import sys

# sets starting variables
# sets board with 2 tiles
grid, score, moved = start_game()

# creates display of board
draw_board(grid, score)

# used to know when to quit running the game
play_again = True

# runs until user exits window or decides not to play again
while play_again:

    # gets user inputs
    for event in pygame.event.get():

        # terminates code when user exits the window
        if event.type == pygame.QUIT:
            sys.exit()

        # user pressed a key
        if event.type == pygame.KEYDOWN:

            # user pressed right arrow 
            # shifts tiles to the right
            if event.key == pygame.K_RIGHT:

                # runs up_slide instead of right_slide
                # because pygames display indexes are rotated on an axis
                grid, score, moved = up_slide(grid, score)

            # user pressed left arrow 
            # shifts tiles to the left
            if event.key == pygame.K_LEFT:

                # runs down_slide instead of left_slide
                # because pygames display indexes are rotated on an axis
                grid, score, moved = down_slide(grid, score)
            
            # user pressed up arrow 
            # shifts tiles up
            if event.key == pygame.K_UP:

                # runs left_slide instead of up_slide
                # because pygames display indexes are rotated on an axis
                grid, score, moved = left_slide(grid, score)
            
            # user pressed down arrow 
            # shifts tiles down
            if event.key == pygame.K_DOWN:

                # runs right_slide instead of down_slide
                # because pygames display indexes are rotated on an axis
                grid, score, moved = right_slide(grid, score)

            # checks if intended slide moved any tiles
            if moved:

                # new random block is placed randomly on board only when a slide occurs
                new_block_location(grid, new_block())

            # updates display board for user to see changes
            draw_board(grid, score)

            # checks if any valid slides are available
            # if not game is over
            if check_end(grid):

                # asks user to play again 
                play_again = game_over()

                if play_again:

                    # resets game variables and board to beginning
                    # displays reset board to play again 
                    grid, score, moved = start_game()
                    draw_board(grid, score)
