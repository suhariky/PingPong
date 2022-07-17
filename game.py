from tkinter import Y
from turtle import window_height
from pygame import *
from random import *
import time as t

#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

class GameSprite(sprite.Sprite):
    def __init__(self, xcor, ycor, width, height, speed, player_image):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = xcor
        self.rect.y = ycor
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        keys = key.get_pressed()

        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

    def update_right(self):
        keys = key.get_pressed()

        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

win_height = 500
win_width = 700
background = transform.scale(image.load("media/forest.jpg"), (win_width, win_height))
window = display.set_mode((win_width, win_height))
window.blit(background, (0, 0))

racket_left_image = "media/player1.JPG"
racket_right_image = "media/player2.JPG"
ball_image = "media/ball.png"

mixer.init()
mixer.music.load("media/Fon.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(loops=-1)
racket_sound = mixer.Sound("media/BallSound.mp3")
win_sound = mixer.Sound("media/Win.mp3")

font.init()
game_font = font.SysFont("Times New Roman", 24)
win_left = game_font.render("PRESS F TO PAY RESPECT VASYA.", True, (255, 255, 255))
win_right = game_font.render("PRESS F TO PAY RESPECT LISA.", True, (255, 255, 255))

timer = time.Clock()
game = True
finish = False
lose = 0

ball_speed_x = randint(-5,5)
ball_speed_y = randint(-5,5)

ball = GameSprite(350, 250, 50, 50, 5, ball_image)
left_racket = Player(30, 200, 50, 150, 5, racket_left_image)
right_racket = Player(520, 200, 50, 150, 5, racket_right_image)

#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        # LOL
        ball.rect.x += randint(-5,5)
        ball.rect.y += randint(-5,5)
        # ball.rect.x += ball_speed_x
        # ball.rect.y += ball_speed_y

        left_racket.update_left()
        right_racket.update_right()

        if ball.rect.y < 5 or ball.rect.y > win_height - 50:
            ball_speed_y *= -1
            racket_sound.play()

        if sprite.collide_rect(ball, left_racket) or sprite.collide_rect(ball, right_racket):
            ball_speed_x *= -1
            racket_sound.play()

        if ball.rect.x < left_racket.rect.x:
            window.blit(win_right, (200,200))
            lose += 1
            finish = True

        if ball.rect.x > right_racket.rect.x:
            window.blit(win_left, (200,200))
            lose += 1
            finish = True

        # if lose == 1:
        #     win_sound.play()

        ball.reset()
        left_racket.reset()
        right_racket.reset()

    else:
        t.sleep(5)
        finish = False
        ball.kill()
        ball = GameSprite(350, 250, 50, 50, 5, ball_image)
        ball_speed_x = randint(-5,5)
        ball_speed_y = randint(-5,5)


    display.update()
    timer.tick(90)