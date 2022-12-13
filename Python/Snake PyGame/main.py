import random
import pygame
import time

pygame.init()

def message(msg,color, x, y, size):
    msg = pygame.font.SysFont(None, size).render(msg, True, color)
    display.blit(msg, [x, y])

display = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Score: 0')

white = (255, 255, 255)
black = (0, 0, 0)
gray = (120, 120, 120)

clock = pygame.time.Clock()

def main_loop():
    count = 0

    curr_x = 200
    curr_y = 150

    change_x = 0
    change_y = 0

    snake_body = []
    snake_length = 0

    food_x = round(random.randrange(0, 390) / 10) * 10
    food_y = round(random.randrange(0, 290) / 10) * 10

    game_over = False
    game_closed = False

    while not game_over:

        while game_closed:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_q):
                        game_over = True
                        game_closed = False
                    elif (event.key == pygame.K_SPACE):
                        game_closed = False
                        main_loop()
             
            if (count % 2 == 0):
                color = white
            else:
                color = gray
            display.fill(black)
            message('You lost!', color, 125, 125, 50)
            message('Press space to play again or q to quit.', white, 70, 165, 21)
            pygame.display.update()
            count += 1
            time.sleep(1)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                game_over = True
            elif (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_LEFT:
                    change_x = -10
                    change_y = 0
                elif event.key == pygame.K_RIGHT:
                    change_x = 10
                    change_y = 0
                elif event.key == pygame.K_UP:
                    change_y = -10
                    change_x = 0
                elif event.key == pygame.K_DOWN:
                    change_y = 10
                    change_x = 0

        curr_x += change_x
        curr_y += change_y

        if (curr_x > 400 or curr_y > 300 or curr_x < 0 or curr_y < 0):
            game_closed = True

        display.fill(black)
        pygame.draw.rect(display, white, [curr_x, curr_y, 10, 10])
        pygame.draw.rect(display, gray, [food_x, food_y, 10, 10])

        snake_body.append((curr_x, curr_y))

        if (curr_x == food_x and curr_y == food_y):
            food_x = round(random.randrange(0, 390) / 10) * 10
            food_y = round(random.randrange(0, 290) / 10) * 10
            snake_length +=1

        for [body_x, body_y] in snake_body[:-1]:
            pygame.draw.rect(display, white, [body_x, body_y, 10, 10])
            if (curr_x == body_x and curr_y == body_y):
                game_closed =True

        if (len(snake_body) > snake_length):
            del snake_body[0]

        pygame.display.update()
        pygame.display.set_caption('Score: %s' %snake_length)
        clock.tick(15)

    pygame.quit()
    quit()

main_loop()