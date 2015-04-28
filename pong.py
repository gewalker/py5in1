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
    pygame.draw.rect(surface,white,[0,64,surfaceWidth - 16,16])
    pygame.draw.rect(surface,white,[surfaceWidth-16,64,16,surfaceHeight-64])
    pygame.draw.rect(surface,white,[0,surfaceHeight-16,surfaceWidth-16,16])

def main():
    blip = pygame.mixer.Sound("pongblip.wav")
    youlose = pygame.mixer.Sound("youlose.wav")
    bloop = pygame.mixer.Sound("pongbloop.wav")
    paddle_ymove = 0
    paddle_ysize = 80
    paddle_xsize = 16
    paddle_xloc = 16
    paddle_yloc = (surfaceHeight/2 + 12)
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
                    paddle_ymove = -5
                if event.key == pygame.K_DOWN:
                    paddle_ymove = 5

            if event.type == pygame.KEYUP:
                paddle_ymove = 0

        if paddle_yloc < 80:
            paddle_yloc = 80
            paddle_ymove = 0
        elif (paddle_yloc + paddle_ysize) > surfaceHeight - 16:
            paddle_yloc = (surfaceHeight - (16 + paddle_ysize))
            paddle_ymove = 0

        if ball_xloc + ball_size >= (surfaceWidth-16):
            print("Collision with rear court.")
            bloop.play()
            ball_xmove = -(ball_xmove)

        if ball_yloc <= 80:
            print("Collision with upper court.")
            bloop.play()
            ball_ymove = -(ball_ymove)

        if ball_yloc + ball_size >= surfaceHeight - 16:
            print("Collision with lower court.")
            bloop.play()
            ball_ymove = -(ball_ymove)

        if ball_xloc <= (paddle_xloc + paddle_xsize):
            if (paddle_yloc <= ball_yloc <= paddle_yloc + paddle_ysize) or (paddle_yloc <= ball_yloc+ball_size <= paddle_yloc + paddle_ysize):
                print("Collison with paddle.")
                blip.play()
                ball_xloc = 33
                ball_xmove = -(ball_xmove)
                ball_ymove = -(ball_ymove) + paddle_ymove

        if ball_xloc < 0:
            print("Ball outside playfield")
            youlose.play()
            time.sleep(3)
            ball_xmove = 6
            ball_ymove = random.randint(-5,5)
            ball_xloc = (surfaceWidth/2)
            ball_yloc = ((surfaceHeight/2)+32)

        paddle_yloc = paddle_yloc + paddle_ymove
        ball_xloc = ball_xloc + ball_xmove
        ball_yloc = ball_yloc + ball_ymove
        print(str(ball_xloc) + ":" + str(ball_xmove) + "  ::  " + str(ball_yloc) + ":" + str(ball_ymove))
        surface.fill(black)
        court()
        paddle(paddle_xloc,paddle_yloc,paddle_xsize,paddle_ysize)
        ball(ball_xloc,ball_yloc,ball_size)
        pygame.display.update()
        clock.tick(120)
main()
pygame.quit()
pygame.mixer.quit()
quit()
