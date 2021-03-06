import pygame
import random
import math
from pygame import mixer

pygame.init()

#Background
screen = pygame.display.set_mode((800,600))

#Background Music
mixer.music.load('Assets/background.wav')
mixer.music.play(-1)

#Caption Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("Assets/space-invaders.png")
pygame.display.set_icon(icon)


#background
background = pygame.image.load("Assets/background_space.png")


#Player
playerImg = pygame.image.load('Assets/playerspace.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Assets/ufospace.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('Assets/bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10 
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font("Assets/space age.ttf",32)

textX = 10
textY = 10

#Game_Over_Text
game_over = pygame.font.Font("Assets/space age.ttf",64)

def player(x, y):
    screen.blit(playerImg,(x ,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i],(x ,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = game_over.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))


#Game loop
running = True
while running:
    screen.fill((0,0,0))

    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -4
            if event.key == pygame.K_d:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bull_sound = mixer.Sound('Assets/laser.wav')
                    bull_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    #boundry
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 440: 
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('Assets/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+=1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150) 
        
        enemy(enemyX[i],enemyY[i], i)

    #bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change 
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"  

    show_score(textX, textY)
    player(playerX, playerY) 
    pygame.display.update()
