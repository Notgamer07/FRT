import pygame
from UI import *
from random import randint
import random
from os.path import join, dirname
from datahandle import Question, save_gameState, get_gameState

__all__ = ['falling_block', 'falling_animation', 'draw_defeat', 
           'draw_label', 'draw_background', 'draw_score', 
           'menu_button', 'draw_victory', 'SettingsUI']

defeat_img = pygame.image.load(join(dirname(__file__),'img','defeated.png'))
defeat_img = pygame.transform.scale(defeat_img, (550,100))
defeat_rect = defeat_img.get_rect()
defeat_rect.center = (400,300)
defeat_img.set_colorkey((255,255,255))

victory_img = pygame.image.load(join(dirname(__file__),"img","VICTORY.png"))
victory_img = pygame.transform.scale(victory_img,(550,100))
victory_rect = victory_img.get_rect()
victory_rect.center = (400,200)
victory_img.set_colorkey((255,255,255))

COLOR= [(255, 87, 87), (177, 90, 255), (50, 205, 50), (255, 223, 0), (255, 20, 147)]
random.shuffle(COLOR)

star_img = pygame.image.load(join(dirname(__file__),'img','star.png'))

star_frames = [] #conatins section of star image, 4 frame of tar from brigth to dim
frame_width = 32
for i in range(4):
    star_rect = pygame.Rect(i*frame_width, 0, frame_width, 32)
    surf = star_img.subsurface(star_rect).copy()
    star_frames.append(surf)

frame_no=[]
for i in range(20):
    ran = randint(0,3)
    frame_no.append(ran)
star_pos  = []
for _ in range(20):
    x = randint(0,800)
    y = randint(0,600)
    star_pos.append((x,y))

def draw_background(screen):
    for i in range(20):
        screen.blit(star_frames[frame_no[i]],star_pos[i])


def falling_block(ques: Question, block_group: pygame.sprite.Group): # this fnc is call by ref so no need for return
    optionText = ques.option[randint(0, 3)]
    x_position = randint(0, 800 - 80)  # screen width - block width
    button = Block(
        x_position, 
        -80, 
        (80, 80),
        text=str(optionText),
        color=COLOR[randint(0, len(COLOR) - 1)],
        bold=True
    )
    block_group.add(button)

def falling_animation(screen, buttons, dt, Speed=200):
    for button in buttons:
        button.fall(Speed * dt)  # smooth float-based movement
        button.draw(screen)    
        
def draw_defeat(screen)->str:
    screen.blit(defeat_img,defeat_rect)
    quitButton = RaisedButton(300,500,(200,60),"QUIT",(250,100,100),(255,50,50), hover = True, autofit=True)
    retry_button = Button(350,400,(100,80),"RETRY",(255, 182, 193),(245, 162, 173),True,autofit=True)
    retry_button.config(bold=True)
    retry_button.draw(screen)
    quitButton.draw(screen)
    if quitButton.isClicked():
        pygame.quit()
        return 'quit'
    if retry_button.isClicked():
        return 'game'
    pygame.display.update()
    return 'defeat'

def draw_label(screen, label):
    # draw white border with padding
    padding = 4
    rect = pygame.Rect(
        label.rect.left - padding,
        label.rect.top - padding,
        label.rect.width + (2*padding),
        label.rect.height + (2*padding)
    )
    pygame.draw.rect(screen, (255,255,255), rect)
    label.draw(screen)

def draw_score(screen,score):
    gm_score = f'SCORE : {score}'
    font = pygame.font.SysFont('Arial',20,True,False) #Arial Bold font of size 20
    text_surf = font.render(gm_score,True,'white',wraplength= 0)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (5,5)
    screen.blit(text_surf,text_rect)

def menu_button():
    startButton = RaisedButton(300,250,(200,60),"START",(100,200,100),(50,255,50),hover=True,autofit=True, bold=True)
    settingsButton = RaisedButton(300,350,(200,60),"SETTINGS",(100,200,250),(50,150,250),hover=True,autofit=True)
    quitButton = RaisedButton(300,450,(200,60),"QUIT",(250,100,100),(255,50,50), hover = True, autofit=True)
    return [startButton, settingsButton, quitButton]

def draw_victory(screen, score : int)->str:
    screen.blit(victory_img,victory_rect)
    retry_button = Button(350,400,(100,80),"RETRY",(255, 182, 193),(245, 162, 173),True,autofit=True)
    quitButton = RaisedButton(300,500,(200,60),"QUIT",(250,100,100),(255,50,50), hover = True, autofit=True)
    retry_button.config(bold=True)
    retry_button.draw(screen)
    quitButton.draw(screen)
    if quitButton.isClicked():
        return 'quit'
    if retry_button.isClicked():
        return 'game'
    font = pygame.font.SysFont(None, 36, bold=True)
    scoreLabel = font.render(f"SCORE :{score}", True, (255,255,255))
    screen.blit(scoreLabel, (400, 300))

    pygame.display.update()
    return 'victory'

class SettingsUI:
    def __init__(self):
        self.game_state = get_gameState()
        self.volume_state = bool(self.game_state.get("Sound", 1))
        self.music_state = bool(self.game_state.get("Music", 1))

        self.volumeButton = None
        self.musicButton = None
        self.backButton = None

    def _create_buttons(self):
        if self.volumeButton is None:
            state = "ON" if self.volume_state else "OFF"
            textColor=(0, 200, 0) if self.volume_state else (200, 0, 0)
            Color=(80, 80, 80) if self.volume_state else (180, 180, 180)
            self.volumeButton = Button(200, 100, (50, 50), state, color=Color,
                                       text_color=textColor, bold=True, autofit=True)
            self.volumeButton.rect.center = (500, 100)

        if self.musicButton is None:
            state = "ON" if self.music_state else "OFF"
            textColor=(0, 200, 0) if self.music_state else (200, 0, 0),
            Color=(80, 80, 80) if self.music_state else (180, 180, 180)
            self.musicButton = Button(200, 100, (50, 50), state, color=Color,
                                      text_color=textColor, bold=True, autofit=True)
            self.musicButton.rect.center = (500, 200)

        if self.backButton is None:
            self.backButton = Button(200, 60, (100, 40), "BACK", (60, 60, 60),
                                     text_color=(255, 255, 255), bold=True,autofit=True)
            self.backButton.rect.center = (400, 320)

    def draw(self, screen):
        self._create_buttons()

        # Draw labels (no Label class)
        font = pygame.font.SysFont(None, 36, bold=True)
        sound_label = font.render("SOUND EFFECT:", True, (255, 255, 255))
        music_label = font.render("MUSIC:", True, (255, 255, 255))

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(95, 65, 310, 70))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(95, 165, 170, 70))

        screen.blit(sound_label, (110, 85))
        screen.blit(music_label, (110, 185))

        self.volumeButton.draw(screen)
        self.musicButton.draw(screen)
        self.backButton.draw(screen)

        # Volume Toggle
        if self.volumeButton.isClicked():
            self.volume_state = not self.volume_state
            self.volumeButton.config(
                text="ON" if self.volume_state else "OFF",
                text_color=(0, 200, 0) if self.volume_state else (200, 0, 0),
                color=(80, 80, 80) if self.volume_state else (180, 180, 180)
            )
            self._update_game_state("Sound", int(self.volume_state))

        # Music Toggle
        if self.musicButton.isClicked():
            self.music_state = not self.music_state
            self.musicButton.config(
                text="ON" if self.music_state else "OFF",
                text_color=(0, 200, 0) if self.music_state else (200, 0, 0),
                color=(80, 80, 80) if self.music_state else (180, 180, 180)
            )
            self._update_game_state("Music", int(self.music_state))

    def _update_game_state(self, key, value):
        self.game_state[key] = value
        save_gameState(self.game_state)

    def back_pressed(self):
        return self.backButton and self.backButton.isClicked()
    