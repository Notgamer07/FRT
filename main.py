import pygame
from front import falling_button, falling_animation, draw_defeat, draw_label, draw_background, draw_score, menu_button
from datahandle import Question
import random

def collision(obj, player, button)->bool:
    if player.colliderect(button.rect):
        if obj.currect == button.text:
            return True
        else:
            return False
    return None


pygame.init()


WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

playerWidth = 90
playerHeight = 20
playerColor = (255,255,255) #white
player = pygame.Rect(WIDTH//2,HEIGHT,playerWidth,playerHeight)
player.center = (WIDTH//2, HEIGHT-(playerHeight//2)- 4 ) # -4 is the padding of the player from the bottom
playerPos = pygame.math.Vector2(player.center)

'''TO HANDLE PLAYER MOVEMENT'''
speed = 400
direction = pygame.math.Vector2(0,0)

score = 0
level = 1
questionNumber = 1

q = Question(level,questionNumber)
buttons = []

menuButtons = menu_button()

run = True
clock = pygame.time.Clock()
current_screen = 'menu'
blocksTime = 0
while run:
    globalTime = pygame.time.get_ticks()
    dt = clock.tick(120) / 1000 #delta time in seconds
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    '''MENU SCREEN'''
    if current_screen == 'menu':
        cooldownTimer = 2000 #2 secons
        draw_background(screen)
        for i,button in enumerate(menuButtons):
            button.draw(screen)
            if button.isClicked():
                if i == 0:
                    current_screen = 'game'
                elif i == 1:
                    current_screen = 'settings'
                else:
                    run = False


        pygame.display.flip()
        continue
    '''DEFEAT SCREEN'''
    if current_screen == 'defeat':
        current_screen=draw_defeat(screen)
        if current_screen == 'game':
            level, questionNumber = 1,1
            q = Question(level, questionNumber)
            buttons = []
        continue
    
    '''GAME SCREEN'''

    #Timer to summon Falling Block
    if (globalTime - blocksTime) >= cooldownTimer:
        blocksTime = pygame.time.get_ticks()
        buttons = falling_button(q, buttons)
        if cooldownTimer >= 1200:
            cooldownTimer = 2000 - (level + questionNumber) * 100
        cooldownTimer += random.randint(0,5)*50  #adding 0.0 to 0.5s randomness in summoning falling blocks

    # Speed of Falling Blocks
    if level < 3 :
        speedOfBlock = 200
    elif level < 6 and speedOfBlock != 240:
        speedOfBlock = 240
    elif level < 9 and level >= 6 and speedOfBlock != 290:
        speedOfBlock = 290
    elif level <=10 and level >= 9 and speedOfBlock != 350:
        speedOfBlock = 350

    # Player Movement
    for button in buttons:
        isCorrect = collision(q,player,button)
        if isCorrect == True:
            score += 1
            if questionNumber<3:
                questionNumber += 1
                q = Question(level,questionNumber)
                buttons.remove(button)
            elif level < 10:
                questionNumber = 1
                level += 1
                questionNumber += 1
                q = Question(level,questionNumber)
                buttons.remove(button)
        elif isCorrect == False:
            current_screen = 'defeat'
            continue

    direction = pygame.math.Vector2(0, 0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.right >= 0: #Pressing Left and player isn't out of bounds of left screen
        direction.x = -1
    elif keys[pygame.K_RIGHT] and player.left <= WIDTH: #Pressing Right and player isn't out of right screen
        direction.x = 1

    playerPos += direction * speed * dt
    player.center = (round(playerPos.x), round(playerPos.y))

    # we draw  background->button ->label->player .. so that player is above button and button is behind label
    draw_background(screen)
    falling_animation(screen,buttons,dt, speedOfBlock)
    draw_label(screen,q.question)
    pygame.draw.rect(screen,playerColor,player,border_radius = 8)
    draw_score(screen,score)

    pygame.display.flip()
pygame.quit()
