#!/usr/bin/env python

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
    pygame.draw.rect(surface, white, [x, y, size, size])


def paddle(x, y, xsize, ysize):
    pygame.draw.rect(surface, white, [x, y, xsize, ysize])


def court():
    pygame.draw.rect(surface, white, [0, 64, surfaceWidth, 16])
    # pygame.draw.rect(surface,white,[surfaceWidth-16,64,16,surfaceHeight-64])
    for y in range(81, (surfaceHeight - 16), 32):
        pygame.draw.rect(surface, grey, [(surfaceWidth / 2) - 8, y, 16, 16])
    pygame.draw.rect(surface, white, [0, surfaceHeight - 16, surfaceWidth, 16])


def sfx():
    blip = pygame.mixer.Sound("pongblip.wav")
    youlose = pygame.mixer.Sound("youlose.wav")
    bloop = pygame.mixer.Sound("pongbloop.wav")
    return (blip, bloop, youlose)

def score_display(score_p1,score_p2):
    numbers = {"0": img0, "1": img1, "2": img2, "3": img3, "4": img4, "5": img5, "6": img6, "7": img7, "8": img8, "9": img9}
    if len(str(score_p1)) > 1:
        surface.blit(numbers[str(score_p1)[0]],(((surfaceWidth / 2) - 80),16))
        surface.blit(numbers[str(score_p1)[1]],(((surfaceWidth / 2) - 48),16))
    else:
        surface.blit(numbers[str(score_p1)[0]],(((surfaceWidth / 2) - 48),16))

    if len(str(score_p2)) > 1:
        surface.blit(numbers[str(score_p2)[0]],(((surfaceWidth / 2) + 16),16))
        surface.blit(numbers[str(score_p2)[1]],(((surfaceWidth / 2) + 48),16))
    else:
        surface.blit(numbers[str(score_p2)[0]],(((surfaceWidth / 2) + 16),16))


def main():
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddlea_ymove = -8
                if event.key == pygame.K_DOWN:
                    paddlea_ymove = 8
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                paddlea_yloc = y

            if event.type == pygame.KEYUP:
                paddlea_ymove = 0

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
         #   score_display(score_p1,score_p2)
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
          #  score_display(score_p1,score_p2)
            time.sleep(3)
            ball_xmove = -6
            ball_ymove = random.randint(-5, 5)
            ball_xloc = (surfaceWidth / 2)
            ball_yloc = ((surfaceHeight / 2) + 32)

        if ball_yloc > (paddleb_yloc + (paddleb_ysize / 2)):
            paddleb_ymove = 8
        elif ball_yloc < paddleb_yloc + (paddleb_ysize / 2):
            paddleb_ymove = -8
        else:
            paddleb_ymove = 0

        paddlea_yloc = paddlea_yloc + paddlea_ymove
        paddleb_yloc = paddleb_yloc + paddleb_ymove
        ball_xloc = ball_xloc + ball_xmove
        ball_yloc = ball_yloc + ball_ymove
        # print(str(ball_xloc) + ":" + str(ball_xmove) + "  ::  " + str(ball_yloc) + ":" + str(ball_ymove))
        surface.fill(black)
        court()
        score_display(score_p1,score_p2)
        paddle(paddlea_xloc, paddlea_yloc, paddlea_xsize, paddlea_ysize)
        paddle(paddleb_xloc, paddleb_yloc, paddleb_xsize, paddleb_ysize)
        ball(ball_xloc, ball_yloc, ball_size)
        pygame.display.update()
        clock.tick(60)


main()
pygame.quit()
pygame.mixer.quit()
quit()
