import pygame
from display_Elements import *
from datahandle import Question
from audio import *
import random
from os.path import dirname, join
from UI import Block, Label


def collision(obj, player, button)->bool:
    # Checks whether the button has collided or not and if collided, is it correct button or not
    # Returns None, if not collided
    # Returns True, if block/button collided and correct block/block.
    # Returns False, if block/butoon collided but incorrect block/block.
    if player.colliderect(button.rect):
        if obj.correct == button.text:
            return True
        else:
            return False
    return None

def heart(lifes): # Draws the Heart on the Screen
    for i in range(lifes):
        health_rect.center = (WIDTH-50-i*22, 20)
        screen.blit(health, health_rect)

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

health = pygame.image.load(join(dirname(__file__), "img", "red-heart.png")).convert_alpha()
health_rect = health.get_rect()
lifes = 3

'''TO HANDLE PLAYER MOVEMENT'''
speed = 400
direction = pygame.math.Vector2(0,0)

score = 0

ques = Question() 
label: Label = Label(
        0, 0, (450, 40), ques.question,
        color=(0,0,0), text_color=(177, 90, 255),
        font=('Arial', 40), bold=True,
        autofit=True
    )
label.rect.center = (400,70)

menuButtons = menu_button()

run = True
clock = pygame.time.Clock()
current_screen = 'menu'
blocksTime = 0
speedOfBlock = 200
all_block = pygame.sprite.Group()
while run:
    globalTime = pygame.time.get_ticks()
    dt = clock.tick(200) / 1000 #delta time in seconds, FPS is set 200 for smooth animation.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    '''MENU SCREEN'''
    if current_screen == 'menu':
        cooldownTimer = 2000 #2 secons
        draw_background(screen)
        for i,block in enumerate(menuButtons):
            block.draw(screen)
            if block.isClicked():
                if i == 0:
                    current_screen = 'game'
                    update_state() # imported form Audio.py. updates audio settings in case nay change is made in the setting after opening up the game
                elif i == 1:
                    current_screen = 'settings'
                    settings = SettingsUI()
                else:
                    run = False


        pygame.display.flip()
        continue

    '''SETTING SCREEN'''
    if current_screen == 'settings':
        draw_background(screen)
        settings.draw(screen)
        if settings.back_pressed():
            current_screen = 'menu'
        pygame.display.flip()
        continue

    '''DEFEAT SCREEN'''
    if current_screen == 'defeat':
        screen.fill((0,0,0))
        draw_background(screen)
        draw_score(screen,score)
        current_screen=draw_defeat(screen)
        if current_screen == 'quit':
            run=False
            break
        elif current_screen == 'game':
            update_state()
            score = 0 # Update the score
            lifes: int = 3 # Refill the lives
            ques.reload_data() # Reload all the data.
            ques.next_question() # Load The question
            label.set_text(ques.question) # Set the question onto the label to change the previously set label
            all_block.empty() # empty all the blocks of the previous game
            falling_block(ques,all_block) # load a new block
        continue
    
    '''VICTORY SCREEN'''
    if current_screen == 'victory':
        screen.fill((0,0,0))
        draw_background(screen)
        current_screen = draw_victory(screen, score)
        if current_screen == 'game':
            update_state()
            score = 0 # Starts the score from 0
            lifes = 3 # Refill The lifes
            ques.reload_data() # Load the 30 question into the class again
            ques.next_question() # Load the question into the object
            label.set_text(ques.question) # reset the label to the lastest question
            all_block.empty() # Delete all the blocks of previous game
            falling_block(ques,all_block) # Load a New Block
        elif current_screen == 'quit':
            break
        continue



    '''GAME SCREEN'''
    # Timer to summon Falling Block
    if (globalTime - blocksTime) >= cooldownTimer:
        blocksTime = pygame.time.get_ticks()
        falling_block(ques, all_block)
        if score >= 27 and cooldownTimer >= 350:
            cooldownTimer = 200 
        elif score > 21 and cooldownTimer >= 800:
             cooldownTimer = 400
        elif score > 9 and cooldownTimer >= 1000:
            cooldownTimer =  800
        elif cooldownTimer >= 1600:
            cooldownTimer = 2000 - (score%7) * 100 # The range of cooldown 1400 - 2000 
        cooldownTimer += random.randint(0,5)*50  #adding 0.0 to 0.5s randomness in summoning falling blocks

    # Speed of Falling Blocks
    if score>=9 and score < 18 and speedOfBlock != 240:
        speedOfBlock = 240
    elif score < 27 and score >= 18 and speedOfBlock != 290:
        speedOfBlock = 290
    elif score >= 27 and speedOfBlock != 350:
        speedOfBlock = 350

    """Collision"""
    collidedBlock : list[Block, bool] =[None, None] # variable to store the collided blocks
    for block in all_block:
        result = collision(ques, player, block) # Checked whether the block has collided or not.. 
        if result is True: 
            collidedBlock = [block, True] # Store the collided button state as correct block
            break
        elif result is False:
            collidedBlock = [block, False] # store the collided button state as incorrect block
            break
    if collidedBlock[0] is not None: # Works when button/block has collided
        if collidedBlock[1] == True: # Correct block/button 
            score += 1 
            play(sfx="ScoreUp")
            try:
                ques.next_question()
                label.set_text(ques.question)
            except IndexError:
                current_screen = "victory"
        elif collidedBlock[1] == False: # Incorrect button collided
            lifes -= 1
            if lifes == 0:
                current_screen = 'defeat'
        all_block.remove(block)

        # Player Movement
    direction = pygame.math.Vector2(0, 0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left >= 0: #Pressing Left and player isn't out of bounds of left screen
        direction.x = -1
    elif keys[pygame.K_RIGHT] and player.right <= WIDTH: #Pressing Right and player isn't out of right screen
        direction.x = 1

    playerPos += direction * speed * dt
    player.center = (round(playerPos.x), round(playerPos.y))

    for block in all_block.copy():  # iterate over a copy
        if block.rect.top > 600:  # if screen height = 600
            all_block.remove(block)

    # we draw  background->button ->label->player .. so that player is above button and button is behind label
    screen.fill((0,0,0))
    draw_background(screen)
    all_block.update(dt, speedOfBlock)
    # Draw all blocks
    all_block.draw(screen)
    draw_label(screen,label)
    pygame.draw.rect(screen,playerColor,player,border_radius = 8)
    draw_score(screen,score)
    heart(lifes)
    pygame.display.flip()
pygame.quit()
