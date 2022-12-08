import pygame
from pygame.locals import *
import copy


def draw_lines(wid, heig, box_x, box_y, scr):
    for i in range(wid):  # draw vertical lines
        if i % box_x == 0 and i != 0:
            pygame.draw.line(scr, (0, 0, 0), (i, 0), (i, 9 * box_y))
            if i % (3 * box_x) == 0:
                pygame.draw.line(scr, (0, 0, 0), (i, 0), (i, 9 * box_y), width=3)

    for i in range(heig):  # draw horizontal lines
        if i % box_y == 0 and i != 0:
            pygame.draw.line(scr, (0, 0, 0), (0, i), (wid, i))
            if i % (3 * box_y) == 0:
                pygame.draw.line(scr, (0, 0, 0), (0, i), (wid, i), width=3)


def find_empty(bo):  # find empty spaces in sudoku grid
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True  # solution is found
    else:
        row, col = find

    for i in range(1, 10):  # attempt to put values into boxes
        if valid(bo, i, (row, col)):  # check if value is valid option
            bo[row][col] = i  # put that value into the board
            if solve(bo):  # calling solve next time with one additional number put in
                return True
            bo[row][col] = 0  # (1) we need to erase first inserted number and try other number
    return False  # if this function returns False that means there is no valid solution so ... (1)


def valid(bo, num, pos):
    for i in range(len(bo[0])):     # check row
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(bo)):    # check column
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3  # check box
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def redraw_board(scr, bo, box_x, box_y):  # draws the board
    setable = []  # list of coordinates that are setable
    font = pygame.font.Font("freesansbold.ttf", int(box_y - 20))  # font initialization
    for i in range(len(bo)):  # walks through col
        for j in range(len(bo[0])):  # walks through rows
            if bo[i][j] == 0:  # append to list if elem = 0 -> its setable
                setable.append((i, j))
            else:  # if not 0 draw it to the board
                num = font.render(str(bo[i][j]), True, (87, 8, 97))
                scr.blit(num, (j * box_x + box_x / 4, i * box_y + box_y / 8))
    return setable


def update_board(num, box_x, box_y, setable, solved, bo):  # update the board with user input
    (mouse_x, mouse_y) = pygame.mouse.get_pos()  # get mouse coordinates
    mouse_x //= box_x  # floor division resulting from 0 to 8
    mouse_y //= box_y  # floor division resulting from 0 to 8

    if (mouse_y, mouse_x) in setable and solved[int(mouse_y)][int(mouse_x)] == num:  # check correctness of input
        bo[int(mouse_y)][int(mouse_x)] = num  # if ok update the board
        return True  # correct input -> do not draw red X
    else:
        return False  # incorrect input -> draw another X


def error_made(scr, err, box_y):
    font = pygame.font.Font("freesansbold.ttf", int(box_y - 20))  # draw red X
    err = font.render("X" * err, True, (255, 0, 0))
    scr.blit(err, (10, 9 * box_y))


def main():
    board = [   # valid sudoku grid
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    size = width, height = (801, 801)  # size of screen window
    box_height = height / 9 - 5  # height of single "box"
    box_width = width / 9  # width of single "box"
    error = 1

    pygame.init()  # initialize all imported pygame modules
    pygame.display.set_caption("Sudoku")
    screen = pygame.display.set_mode(size)  # set size of screen window

    screen.fill((106, 90, 205))  # background color
    draw_lines(width, height, box_width, box_height, screen)  # draw lines

    solved_board = copy.deepcopy(board)
    solve(solved_board)  # solve given sudoku to check correctness of user input
    running = True

    while running:  # main loop
        empty = redraw_board(screen, board, box_width, box_height)  # draw board and get coordinates of empty boxes

        for event in pygame.event.get():  # get events from the queue
            if event.type == QUIT:  # if event is quit
                running = False  # exit while loop
            if event.type == pygame.KEYDOWN:  # all keys on keyboard
                if event.key == pygame.K_1:  # number 1 pressed
                    if not update_board(1, box_width, box_height, empty, solved_board, board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
                if event.key == pygame.K_2:
                    if not update_board(2, box_width, box_height, empty, solved_board,
                                        board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
                if event.key == pygame.K_3:
                    if not update_board(3, box_width, box_height, empty, solved_board,
                                        board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
                if event.key == pygame.K_4:
                    if not update_board(4, box_width, box_height, empty, solved_board,
                                        board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
                if event.key == pygame.K_5:
                    if not update_board(5, box_width, box_height, empty, solved_board,
                                        board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
                if event.key == pygame.K_6:
                    if not update_board(6, box_width, box_height, empty, solved_board,
                                        board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
                if event.key == pygame.K_7:
                    if not update_board(7, box_width, box_height, empty, solved_board,
                                        board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
                if event.key == pygame.K_8:
                    if not update_board(8, box_width, box_height, empty, solved_board,
                                        board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
                if event.key == pygame.K_9:
                    if not update_board(9, box_width, box_height, empty, solved_board,
                                        board):  # function call with valid argument
                        error_made(screen, error, box_height)
                        error += 1
        pygame.display.update()  # update display

    pygame.quit()  # uninitialize all pygame modules


if __name__ == '__main__':
    main()
