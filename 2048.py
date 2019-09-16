from functions_2048 import *
import sys

grid, score, moved = start_game()

draw_board(grid, score)

play_again = True
while play_again:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                grid, score, moved = up_slide(grid, score)
            if event.key == pygame.K_LEFT:
                grid, score, moved = down_slide(grid, score)
            if event.key == pygame.K_UP:
                grid, score, moved = left_slide(grid, score)
            if event.key == pygame.K_DOWN:
                grid, score, moved = right_slide(grid, score)
            if moved:
                new_block_location(grid, new_block())
            draw_board(grid, score)
            if check_end(grid):
                play_again = game_over()
                if play_again:
                    grid, score, moved = start_game()
                    draw_board(grid, score)
