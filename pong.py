#!/usr/bin/env python

import pygame
import random
import time

black = (0,0,0)
white = (255,255,255)

pygame.init()
pygame.mixer.init()

surfaceWidth = 800
surfaceHeight = 600

surface = pygame.display.set_mode((surfaceWidth,surfaceHeight))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

def ball(x,y,size):
    pygame.draw.rect(surface,white,[x,y,size,size])

def paddle(x,y,xsize,ysize):
    pygame.draw.rect(surface,white,[x,y,xsize,ysize])

def court():
    pygame.draw.rect(surface,white,[0,64,surfaceWidth,16])
#    pygame.draw.rect(surface,white,[surfaceWidth-16,64,16,surfaceHeight-64])
    pygame.draw.rect(surface,white,[0,surfaceHeight-16,surfaceWidth,16])

def main():
    blip = pygame.mixer.Sound("pongblip.wav")
    youlose = pygame.mixer.Sound("youlose.wav")
    bloop = pygame.mixer.Sound("pongbloop.wav")
    paddlea_ymove = 0
    paddlea_ysize = 80
    paddlea_xsize = 16
    paddlea_xloc = 16
    paddlea_yloc = (surfaceHeight/2 + 12)
    paddleb_ymove = 0
    paddleb_ysize = 80
    paddleb_xsize = 16
    paddleb_xloc = (surfaceWidth - 32)
    paddleb_yloc = (surfaceHeight/2 + 12)
    ball_size = 16
    ball_xmove = 6
    ball_ymove = random.randint(-5,5)
    ball_xloc = (surfaceWidth/2)
    ball_yloc = ((surfaceHeight/2)+32)
    game_over = False
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddlea_ymove = -8
                if event.key == pygame.K_DOWN:
                    paddlea_ymove = 8

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

#        if ball_xloc + ball_size >= (surfaceWidth-16):
#            print("Collision with rear court.")
#            bloop.play()
#            ball_xmove = -(ball_xmove)

        if ball_yloc <= 80:
            print("Collision with upper court.")
            bloop.play()
            ball_ymove = -(ball_ymove)

        if ball_yloc + ball_size >= surfaceHeight - 16:
            print("Collision with lower court.")
            bloop.play()
            ball_ymove = -(ball_ymove)

        if ball_xloc >= (paddleb_xloc):
            if (paddleb_yloc <= ball_yloc <= paddleb_yloc + paddleb_ysize) or (paddleb_yloc <= ball_yloc+ball_size <= paddleb_yloc + paddleb_ysize):
                print("Collison with paddleb.")
                blip.play()
                ball_xloc = (surfaceWidth - 33)
                ball_xmove = -(ball_xmove)
                ball_ymove = -(ball_ymove) + paddleb_ymove

        if ball_xloc <= (paddlea_xloc + paddlea_xsize):
            if (paddlea_yloc <= ball_yloc <= paddlea_yloc + paddlea_ysize) or (paddlea_yloc <= ball_yloc+ball_size <= paddlea_yloc + paddlea_ysize):
                print("Collison with paddlea.")
                blip.play()
                ball_xloc = 33
                ball_xmove = -(ball_xmove)
                ball_ymove = -(ball_ymove) + paddlea_ymove

        if ball_xloc < 0 or ball_xloc > surfaceWidth:
            print("Ball outside playfield")
            youlose.play()
            time.sleep(3)
            ball_xmove = 6
            ball_ymove = random.randint(-5,5)
            ball_xloc = (surfaceWidth/2)
            ball_yloc = ((surfaceHeight/2)+32)

        if ball_yloc > (paddleb_yloc + paddleb_ysize):
            paddleb_ymove = 6
        elif ball_yloc < paddleb_yloc:
            paddleb_ymove = -6
        else:
            paddleb_ymove = 0

        paddlea_yloc = paddlea_yloc + paddlea_ymove
        paddleb_yloc = paddleb_yloc + paddleb_ymove
        ball_xloc = ball_xloc + ball_xmove
        ball_yloc = ball_yloc + ball_ymove
        print(str(ball_xloc) + ":" + str(ball_xmove) + "  ::  " + str(ball_yloc) + ":" + str(ball_ymove))
        surface.fill(black)
        court()
        paddle(paddlea_xloc,paddlea_yloc,paddlea_xsize,paddlea_ysize)
        paddle(paddleb_xloc,paddleb_yloc,paddleb_xsize,paddleb_ysize)
        ball(ball_xloc,ball_yloc,ball_size)
        pygame.display.update()
        clock.tick(60)
main()
pygame.quit()
pygame.mixer.quit()
quit()
