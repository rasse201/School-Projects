import pygame
import time
import random
from datetime import datetime

pygame.init()
display = pygame.display.set_mode((300, 690))

state = 'start'

white = (255, 255, 255)
black = (0, 0, 0)
dark_grey = (10, 10, 10)
white_transparent = (50, 255, 255, 255)
gray = (120, 120, 120)

class Shapes:
    o_shape = [[(1, 1), (1, 2), (2, 1), (2, 2)]]
    i_shape = [[(2, 0), (2, 1), (2, 2), (2, 3)], [(0, 2), (1, 2), (2, 2), (3, 2)]]
    s_shape = [[(2, 1), (3, 1), (1, 2), (2, 2)], [(2, 0), (2, 1), (3, 1), (3, 2)]]
    z_shape = [[(1, 1), (2, 1), (2, 2), (3, 2)], [(3, 0), (3, 1), (2, 1), (2, 2)]]
    j_shape = [[(0, 1), (1, 1), (2, 1), (2, 2)], [(1, 0), (1, 1), (1, 2), (0, 2)], [(0, 2), (1, 2), (2, 2), (0, 1)], [(1, 0), (1, 1), (1, 2), (2, 0)]]
    l_shape = [[(0, 1), (1, 1), (2, 1), (0, 2)], [(0, 0), (1, 0), (1, 1), (1, 2)], [(0, 2), (1, 2), (2, 2), (2, 1)], [(1, 0), (1, 1), (1, 2), (2, 2)]]
    t_shape = [[(0, 1), (1, 1), (2, 1), (1, 2)], [(0, 1), (1, 0), (1, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (2, 1)]]
    shape_names = ['o_shape', 'i_shape', 's_shape', 'z_shape', 'j_shape', 't_shape', 'l_shape']

class Shape_Color:
    o_shape = [71, 92, 81]
    i_shape = [72, 133, 101]
    s_shape = [92, 181, 135]
    z_shape = [116, 212, 162]
    j_shape = [25, 148, 84]
    t_shape = [21, 194, 104]
    l_shape = [16, 232, 120]

class Game_Methods:
    def draw_shape(Curr_Shape):
        for x, y in getattr(Shapes, Curr_Shape.shape_name)[Curr_Shape.rotation]:
            pygame.draw.rect(display, Curr_Shape.color, [Curr_Shape.x + x * 30, Curr_Shape.y + y * 30, 30, 30])

    def move_right(Curr_Shape, board):
        for x, y in getattr(Shapes, Curr_Shape.shape_name)[Curr_Shape.rotation]:
            if Curr_Shape.x + x * 30 == 300 - 30:
                return 0
            elif board[int((Curr_Shape.y + y * 30) / 30)][int((Curr_Shape.x + x * 30 + 30) / 30)] == 1:
                return 0
        return 30

    def move_left(Curr_Shape, board):
        for x, y in getattr(Shapes, Curr_Shape.shape_name)[Curr_Shape.rotation]:
            if Curr_Shape.x + x * 30 == 0:
                return 0
            elif board[int(((Curr_Shape.y + y * 30) / 30))][int((Curr_Shape.x + x * 30 - 30) / 30)] == 1:
                return 0
        return - 30

    def can_move_down(Curr_Shape, board):
        for x, y in getattr(Shapes, Curr_Shape.shape_name)[Curr_Shape.rotation]:
            if board[int((Curr_Shape.y + y * 30 + 30) / 30)][int((Curr_Shape.x + x * 30) / 30)] == 1:
                return False
        return True

    def set_check(Curr_Shape, last_drop, board, board_color, state):
        if time.time() - last_drop > 1.5:
            for x, y in getattr(Shapes, Curr_Shape.shape_name)[Curr_Shape.rotation]:
                if board[int((Curr_Shape.y + y * 30) / 30)][int((Curr_Shape.x + x * 30) / 30)] == 2:
                    state = 'fail'
                board[int((Curr_Shape.y + y * 30) / 30)][int((Curr_Shape.x + x * 30) / 30)] = 1
                board_color[int((Curr_Shape.y + y * 30) / 30)][int((Curr_Shape.x + x * 30) / 30)] = Curr_Shape.color
            if state != 'fail':
                Game_Methods.new_shape(Curr_Shape)
            return board, time.time(), board_color, state
        else:   
            return board, last_drop, board_color, state

    def draw_board(Curr_Shape, board, board_color):
        y_mod = 0
        for x in range(int(300 / 30)):
            if x % 2 == 0:
                y_mod = 0
            else:
                y_mod = 1
            for y in range(int(690 / 30)):
                if y % 2 == y_mod:
                    pygame.draw.rect(display, dark_grey, [x * 30, y * 30, 30, 30])

        for y, row in enumerate(board[:-1]):
            for x, num in enumerate(row):
                if num == 1:
                    pygame.draw.rect(display, board_color[y][x], [x * 30, y * 30, 30, 30])

        s = pygame.Surface((300,120))
        s.set_alpha(30)
        s.fill(white)
        display.blit(s, (0,0))

    def one_down(Curr_Shape, board):
        if Game_Methods.can_move_down(Curr_Shape, board):
            return 30
        return 0

    def drop(Curr_Shape, board):
        while Game_Methods.can_move_down(Curr_Shape, board):
            Curr_Shape.y += 30
        return Curr_Shape.y

    def new_shape(Curr_Shape):
        Curr_Shape.x = 90
        Curr_Shape.y = 0
        Curr_Shape.rotation = 0
        Curr_Shape.shape_name = Shapes.shape_names[random.randint(0, len(Shapes.shape_names) -1)]
        Curr_Shape.color = getattr(Shape_Color, Curr_Shape.shape_name)

    def rotate(Curr_Shape, board):
        last_rotation = Curr_Shape.rotation
        if len(getattr(Shapes, Curr_Shape.shape_name)) == last_rotation +1:
            Curr_Shape.rotation = 0
        else:
            Curr_Shape.rotation += 1
        
        for x, y in getattr(Shapes, Curr_Shape.shape_name)[Curr_Shape.rotation]:
            if Curr_Shape.x + x * 30 < 0 or Curr_Shape.x + x * 30 > 270:
                return last_rotation

        for x, y in getattr(Shapes, Curr_Shape.shape_name)[Curr_Shape.rotation]:
            if board[int((Curr_Shape.y + y * 30) / 30)][int((Curr_Shape.x + x * 30) / 30)] == 1:
                return last_rotation
        return Curr_Shape.rotation

    def check_rows_and_score(board, score, speed_level):
        for i, row in enumerate(board[:-1]):
            if row == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
                board[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                score += 10
                speed_level += 4
        return board, score, speed_level

    def text(text, color, coords, font_size):
        msg = pygame.font.SysFont(None, font_size).render(text, True, color)
        display.blit(msg, coords)
        
def gameLoop(state):
    pygame.display.set_caption('Score: 0')

    global score
    score = 0
    speed_level = 24
    board = [[2 for x in range(10)] for x in range(4)] + [[0 for x in range(10)] for x in range(19)] + [[1 for x in range(10)]]
    board_color = [[[] for x in range(10)] for x in range(23)]

    class Curr_Shape:  
        x = None
        y = None
        rotation = None
        shape_name = None
        color = None

    clock = pygame.time.Clock()
    last_drop = time.time()

    Game_Methods.new_shape(Curr_Shape)

    while state == 'running':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    Curr_Shape.x += Game_Methods.move_right(Curr_Shape, board)
                elif event.key == pygame.K_LEFT:
                    Curr_Shape.x += Game_Methods.move_left(Curr_Shape, board)
                elif event.key == pygame.K_UP:
                    Curr_Shape.rotation = Game_Methods.rotate(Curr_Shape, board)
                elif event.key == pygame.K_DOWN:
                    Curr_Shape.y += Game_Methods.one_down(Curr_Shape, board)
                elif event.key == pygame.K_SPACE:
                    Curr_Shape.y = Game_Methods.drop(Curr_Shape, board)

        if time.time() - last_drop > 10 / speed_level:
            if Game_Methods.can_move_down(Curr_Shape, board):
                last_drop = time.time()
                Curr_Shape.y += 30

        board, last_drop, board_color, state = Game_Methods.set_check(Curr_Shape, last_drop, board, board_color, state)

        board, score, speed_level = Game_Methods.check_rows_and_score(board, score, speed_level)
        display.fill(black)

        Game_Methods.draw_board(Curr_Shape, board, board_color)
        Game_Methods.draw_shape(Curr_Shape)

        pygame.display.set_caption('Score: %s'%score)
        pygame.display.update()
        clock.tick(30)

while state == 'start':
    pygame.display.set_caption('Welcome!')
    
    display.fill(black)

    dt = datetime.now()

    y_mod = 0
    for x in range(int(300 / 30)):
        if x % 2 == 0:
            y_mod = 0
        else:
            y_mod = 1
        for y in range(int(690 / 30)):
            if y % 2 == y_mod:
                pygame.draw.rect(display, dark_grey, [x * 30, y * 30, 30, 30])

    Game_Methods.text('Tetris', white, [60, 100], 95)

    Game_Methods.text('Controls:', white, [10, 500], 20)
    Game_Methods.text('Space To Drop', white, [10, 520], 20)
    Game_Methods.text('Left And Right Arrows To Move', white, [10, 540], 20)
    Game_Methods.text('Down Arrow To Drop One Block', white, [10, 560], 20)
    Game_Methods.text('Up Arrow To Rotate', white, [10, 580], 20)

    if round(dt.timestamp()) % 2 == 0:
        Game_Methods.text('Press Space', white, [90, 180], 30)
    else:
        Game_Methods.text('Press Space', gray, [90, 180], 30)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state = 'running'
                gameLoop(state)
                state = 'fail'


while state == 'fail':
    s = pygame.Surface((300,690))
    s.set_alpha(128)
    s.fill(black)
    display.blit(s, (0,0))

    Game_Methods.text('You Lost..', white, [30, 150], 75)
    Game_Methods.text('Final Score: %s' %score, white, [75, 210], 30)

    Game_Methods.text('Press Space To Try Again:', white, [10, 500], 20)
    Game_Methods.text('Or', white, [10, 520], 20)
    Game_Methods.text('Q To Quit', white, [10, 540], 20)

    restart = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = 'running'
                    gameLoop(state)
                    state = 'fail'
                    restart = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        if restart:
            break
        pygame.display.update()

pygame.quit()
quit()