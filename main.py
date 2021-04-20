import pygame
import random
import math
from pygame import mixer

# initialise the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background .png')

# backgroud sound
mixer.music.load("backgroundmusic.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('spaceship (1).png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('player.png')
playerx = 370
playery = 480
playerx_change = 0
playery_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
no_of_enemies = 4

for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(2)
    enemyy_change.append(2)

# bullet
bulletimg = pygame.image.load('missile.png')
bulletx = 370
bullety = 480
bulletx_change = 0
bullety_change = 10

# ready - you cant see the bullet on the screen
# fire - bullet is currently moving
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('full Pack 2025.ttf', 32)
textx = 10
texty = 10

#game over text
over_font = pygame.font.Font('full Pack 2025.ttf', 64)


def show_score(x, y):
    score = font.render("Score - " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(x,y):
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(score_value, (x,y))



def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# function for bullet fire
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


# collision function
def iscollision(enemyx, enemyy, bullets, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB color assign to background (RED GREEN BLUE)
    screen.fill((0, 255, 255))

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it is right of left
        if event.type == pygame.KEYDOWN:
            print("A keystroke has been pressed")
            if event.key == pygame.K_LEFT:
                playerx_change = -5
                print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
                print("Right arrow is pressed")
            if event.key == pygame.K_UP:
                playery_change = 5
            if event.key == pygame.K_DOWN:
                playery_change = -5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('bullet.wav')
                    bullet_sound.play()
                    # get current x coordinate of the spaceship
                    bulletx = playerx
                    bullety = playery
                    fire_bullet(bulletx, playery)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playery_change = 0

                print("Keystroke has been released")
    # checking for boundaries of spaceship so it dosent go out
    playerx += playerx_change
    playery -= playery_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    if playery <= 0:
        playery = 0
    elif playery >= 536:
        playery = 536

    # enemy movement
    for i in range(no_of_enemies):

        #game over
        if enemyx == playerx and enemyy == playery :
            for j in range (no_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break


        enemyx[i] += enemyx_change[i]
        enemyy[i] += enemyy_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 2
        elif enemyx[i] >= 736:
            enemyx_change[i] = -2
        if enemyy[i] <= 0:
            enemyy_change[i] = 2
        elif enemyy[i] >= 536:
            enemyy_change[i] = -2

        # collision detection
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = playery
            bulletx = playerx
            bullet_state = "ready"
            score_value += 1

            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
