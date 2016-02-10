#!/usr/bin/env python
"""Python pong/4 in 1 or 5 in 1 tv game sim."""

import pygame
import random
import time
from math import copysign

black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)

pygame.init()
pygame.mixer.init()

surfaceWidth = 800
surfaceHeight = 600

surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))
pygame.display.set_caption("Pong")
img0 = pygame.image.load("numbers/0.png")
img1 = pygame.image.load("numbers/1.png")
img2 = pygame.image.load("numbers/2.png")
img3 = pygame.image.load("numbers/3.png")
img4 = pygame.image.load("numbers/4.png")
img5 = pygame.image.load("numbers/5.png")
img6 = pygame.image.load("numbers/6.png")
img7 = pygame.image.load("numbers/7.png")
img8 = pygame.image.load("numbers/8.png")
img9 = pygame.image.load("numbers/9.png")
clock = pygame.time.Clock()


def ball(x, y, size):
    """Draw the ball."""
    pygame.draw.rect(surface, white, [x, y, size, size])


def paddle(x, y, xsize, ysize):
    """Draw the paddle."""
    pygame.draw.rect(surface, white, [x, y, xsize, ysize])


def court():
    """Draw the boundaries of the court."""
    pygame.draw.rect(surface, white, [0, 64, surfaceWidth, 16])
    # pygame.draw.rect(surface,white,[surfaceWidth-16,64,16,surfaceHeight-64])
    for y in range(81, (surfaceHeight - 16), 32):
        pygame.draw.rect(surface, grey, [(surfaceWidth / 2) - 8, y, 16, 16])
    pygame.draw.rect(surface, white, [0, surfaceHeight - 16, surfaceWidth, 16])


def sfx():
    """Define sound effects."""
    blip = pygame.mixer.Sound("pongblip.wav")
    youlose = pygame.mixer.Sound("youlose.wav")
    bloop = pygame.mixer.Sound("pongbloop.wav")
    return (blip, bloop, youlose)


def score_display(score_p1, score_p2):
    """Display the score."""
    numbers = {"0": img0, "1": img1, "2": img2, "3": img3, "4": img4, "5": img5, "6": img6, "7": img7, "8": img8, "9": img9}
    if len(str(score_p1)) > 1:
        surface.blit(numbers[str(score_p1)[0]], (((surfaceWidth / 2) - 80), 16))
        surface.blit(numbers[str(score_p1)[1]], (((surfaceWidth / 2) - 48), 16))
    else:
        surface.blit(numbers[str(score_p1)[0]], (((surfaceWidth / 2) - 48), 16))

    if len(str(score_p2)) > 1:
        surface.blit(numbers[str(score_p2)[0]], (((surfaceWidth / 2) + 16), 16))
        surface.blit(numbers[str(score_p2)[1]], (((surfaceWidth / 2) + 48), 16))
    else:
        surface.blit(numbers[str(score_p2)[0]], (((surfaceWidth / 2) + 16), 16))


def slope_and_intercept(pre_ball_loc, post_ball_loc):
    """Based on the ball's position, calculate the slope and y-axis intercept of the ball's present course."""
    prex, prey = pre_ball_loc
    postx, posty = post_ball_loc
    m = (posty - prey)/(postx - prex)
    b = (posty - (m * postx))
    print(str(b))
    return m, b


def computer_move_paddle(pre_ball_loc, post_ball_loc, paddleb_yloc):
    """Calculate the computer's paddle movement."""
    prex, prey = pre_ball_loc
    postx, posty = post_ball_loc
    prex = (surfaceWidth - 32) - prex
    postx = (surfaceWidth - 32) - postx
    m, b = slope_and_intercept((prex, prey), (postx, posty))
    if paddleb_yloc + (32) < b and (paddleb_yloc + 32) < (surfaceHeight - 16):
        print("Predicted impact: " + str(b) + " " + "Paddle ctr: " + str(paddleb_yloc))
        return 8
    elif paddleb_yloc + (32) > b and paddleb_yloc > 80:
        return -8
    else:
        return 0


def main():
    """Main.  Seriously.  Main."""
    blip, bloop, youlose = sfx()
    paddlea_ymove = 0
    paddlea_ysize = 80
    paddlea_xsize = 16
    paddlea_xloc = 16
    paddlea_yloc = (surfaceHeight / 2 + 12)
    paddleb_ymove = 0
    paddleb_ysize = 80
    paddleb_xsize = 16
    paddleb_xloc = (surfaceWidth - 32)
    paddleb_yloc = (surfaceHeight / 2 + 12)
    score_p1 = 0
    score_p2 = 0
    ball_size = 16
    ball_xmove = 6
    ball_ymove = random.randint(-5, 5)
    ball_xloc = (surfaceWidth / 2)
    ball_yloc = ((surfaceHeight / 2) + 40)
    game_over = False
    pygame.mouse.set_visible(False)
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                paddlea_yloc = y

        if paddlea_yloc < 80:
            paddlea_yloc = 80
            paddlea_ymove = 0
        elif (paddlea_yloc + paddlea_ysize) > surfaceHeight - 16:
            paddlea_yloc = (surfaceHeight - (16 + paddlea_ysize))
            paddlea_ymove = 0

        if paddleb_yloc < 80:
            paddleb_yloc = 80
            paddleb_ymove = 0
        elif (paddleb_yloc + paddleb_ysize) > surfaceHeight - 16:
            paddleb_yloc = (surfaceHeight - (16 + paddleb_ysize))
            paddleb_ymove = 0

        # if ball_xloc + ball_size >= (surfaceWidth-16):
        #            print("Collision with rear court.")
        #            bloop.play()
        #            ball_xmove = -(ball_xmove)

        if ball_yloc <= 80:
            print("Collision with upper court.")
            bloop.play()
            ball_yloc = 81
            ball_ymove = -(ball_ymove)

        if ball_yloc + ball_size >= surfaceHeight - 16:
            print("Collision with lower court.")
            bloop.play()
            ball_yloc = surfaceHeight - (17 + ball_size)
            ball_ymove = -(ball_ymove)

        if ball_xloc >= (paddleb_xloc):
            if (paddleb_yloc <= ball_yloc <= paddleb_yloc + paddleb_ysize) or (
                            paddleb_yloc <= ball_yloc + ball_size <= paddleb_yloc + paddleb_ysize):
                print("Collison with paddleb.")
                blip.play()
                ball_xloc = (surfaceWidth - 33)
                ball_xmove = -(ball_xmove)
                ball_ymove = -(ball_ymove) + paddleb_ymove

        if ball_xloc <= (paddlea_xloc + paddlea_xsize):
            if (paddlea_yloc <= ball_yloc <= paddlea_yloc + paddlea_ysize) or (
                            paddlea_yloc <= ball_yloc + ball_size <= paddlea_yloc + paddlea_ysize):
                print("Collison with paddlea.")
                blip.play()
                ball_xloc = 33
                x, y = pygame.mouse.get_rel()
                print("relative mouse speed: " + str(y))
                ball_xmove = -(ball_xmove)
                if abs(-(ball_ymove) + (y * 0.05)) > 20:
                    trunc_move = copysign(20, (-(ball_ymove) + (y * 0.05)))
                    ball_ymove = -(trunc_move)
                else:
                    ball_ymove = (ball_ymove) + (y * 0.05)
                print(str(ball_ymove))

        if ball_xloc < 0:
            print("Ball outside playfield")
            youlose.play()
            score_p2 += 1
            print("Score: " + str(score_p1) + " | " + str(score_p2))
            # score_display(score_p1,score_p2)
            time.sleep(3)
            ball_xmove = 6
            ball_ymove = random.randint(-5, 5)
            ball_xloc = (surfaceWidth / 2)
            ball_yloc = ((surfaceHeight / 2) + 32)

        if ball_xloc > surfaceWidth:
            print("Ball outside playfield")
            youlose.play()
            score_p1 += 1
            print("Score: " + str(score_p1) + " | " + str(score_p2))
            # score_display(score_p1,score_p2)
            time.sleep(3)
            ball_xmove = -6
            ball_ymove = random.randint(-5, 5)
            ball_xloc = (surfaceWidth / 2)
            ball_yloc = ((surfaceHeight / 2) + 32)

# Smarter computer paddle moves

        pre_ball_loc = (ball_xloc, ball_yloc)
        paddlea_yloc = paddlea_yloc + paddlea_ymove
        #     paddleb_yloc = paddleb_yloc + paddleb_ymove
        ball_xloc = ball_xloc + ball_xmove
        ball_yloc = ball_yloc + ball_ymove
        post_ball_loc = (ball_xloc, ball_yloc)
        print(str(pre_ball_loc) + ":" + str(post_ball_loc))
        paddleb_ymove = computer_move_paddle(pre_ball_loc, post_ball_loc, paddleb_yloc)
        paddleb_yloc = paddleb_yloc + int(paddleb_ymove)
        # print(str(ball_xloc) + ":" + str(ball_xmove) + "  ::  " + str(ball_yloc) + ":" + str(ball_ymove))
        surface.fill(black)
        court()
        score_display(score_p1, score_p2)
        paddle(paddlea_xloc, paddlea_yloc, paddlea_xsize, paddlea_ysize)
        paddle(paddleb_xloc, paddleb_yloc, paddleb_xsize, paddleb_ysize)
        ball(ball_xloc, ball_yloc, ball_size)
        pygame.display.update()
        clock.tick(60)


main()
pygame.quit()
pygame.mixer.quit()
quit()
