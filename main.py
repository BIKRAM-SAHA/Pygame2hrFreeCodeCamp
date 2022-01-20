import pygame
import random
import math
from pygame import mixer

#initialise the pygame
pygame.init()

#creating the screen
screen = pygame.display.set_mode((800,600))

#Title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#background image
bgImage=pygame.image.load("background.png")
#background music
mixer.music.load("background.wav")
mixer.music.play(-1)

#maintain score
score=0
textX=10
textY=10
font=pygame.font.SysFont('freesansbold.ttf',32) #font object (family, size, bold, italic)
def showScore(x,y):
    #fonts need to be redered
    scorefont=font.render("Score: "+str(score),True,(255,255,255)) #(text,whether to show,color)
    #then blited to screen
    screen.blit(scorefont,(x,y))
#gameOver
overFont=pygame.font.SysFont('freesansbold.ttf',64) #font object
def gameOver():
    overtext=overFont.render("GAME OVER",True,(255,210,150))
    finalScoretext=overFont.render("Score: "+str(score),True,(255,210,150))
    screen.blit(overtext,(250,250))
    screen.blit(finalScoretext,(300,320))

#player
playerImg=pygame.image.load('player.png')
playerX=370 
playerY=480
playerChange=0

def player():
    screen.blit(playerImg,(playerX,playerY))

#enemy
enemyImg=pygame.image.load('enemy.png')
enemyX=[]
enemyY=[]
enemyXChange=[]
enemyYChange=[]
noOfEnemies=5
for i in range(noOfEnemies):
    # enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(20, 200))
    enemyXChange.append(float(random.choice(['+','-'])+str(random.random()*2+1)))
    enemyYChange.append(15)

def enemy(i):
    screen.blit(enemyImg,(enemyX[i],enemyY[i]))

#bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletXChange=0
bulletYChange=5
bulletState="ready"

def bullet():
    screen.blit(bulletImg,(bulletX,bulletY))
def fireBulet(x,y):
    global bulletState
    bulletState="fire"
    screen.blit(bulletImg,(x+16,y+10))
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<27 and bulletState=="fire":
        return True
    return False

#game loop
running = True
while running:
    #change background color
    screen.fill((54, 69, 79))
    #background image
    screen.blit(bgImage,(0,0))
    #display score
    showScore(textX,textY)

    #adding quit method to stop program when quit event occurs or else the game is hanged by win
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            running=False

        #if keystroke is pressed
        if(event.type==pygame.KEYDOWN):
            #if its a -> or <- direction key
            if(event.key==pygame.K_LEFT):
                playerChange=-3
            elif(event.key==pygame.K_RIGHT):
                playerChange=3
            #if its a SPACE
            elif(event.key==pygame.K_SPACE or event.key==pygame.K_RETURN):
                if(bulletState=="ready"):
                    bulletX=playerX
                    fireBulet(bulletX, bulletY)
                    #bullet sound
                    bulletSound=mixer.Sound("laser.wav")
                    bulletSound.play()
            else:
                playerChange=0
        if(event.type==pygame.KEYUP):
            #if its a -> or <- direction key
            if(event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT):
                playerChange=0

    #player position update
    playerX+=playerChange
    if(playerX<=0):
        playerX=0
    elif(playerX>=737):
        playerX=737

    #adding player to screen ->makesure it is called after screen.fill() or else player will be drawn beneath the screen fill
    player()

    #enemy position update
    for i in range(noOfEnemies):
        #check for game over
        if(enemyY[i]>420):
            noOfEnemies=0
            break
        #adding enemy to screen
        enemy(i)
        enemyX[i]+=enemyXChange[i]
        if(enemyX[i]<=0):
            enemyXChange[i]=-enemyXChange[i]
            enemyY[i]+=enemyYChange[i]
        elif(enemyX[i]>=737):
            enemyXChange[i]=-enemyXChange[i]
            enemyY[i]+=enemyYChange[i]
        #collision check
        collision=isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if(collision):
            bulletY=480
            bulletState="ready"
            score+=1
            enemyX[i]=random.randint(0, 736)
            enemyY[i]=random.randint(50, 150)
            #collision sound
            collisionSound=mixer.Sound("explosion.wav")
            collisionSound.play()

    if(noOfEnemies==0):gameOver()

    #bullet animation
    if bulletY<0:
        bulletY=480
        bulletState="ready"
    if(bulletState == "fire"):
        fireBulet(bulletX, bulletY)
        bulletY-=bulletYChange

    #update the display
    pygame.display.update()