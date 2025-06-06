import pygame
from package import Label,Button
from random import randint
import random
from os.path import join, dirname

defeat_img = pygame.image.load(join(dirname(__file__),'img','defeated.png'))
defeat_img = pygame.transform.scale(defeat_img, (550,100))
defeat_rect = defeat_img.get_rect()
defeat_rect.center = (400,300)
defeat_img.set_colorkey((255,255,255))

Colors= [(255, 87, 87), (177, 90, 255), (50, 205, 50), (255, 223, 0), (255, 20, 147)]
random.shuffle(Colors)

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


def falling_button(optionText):
    listOfButton = []
    for i in range(len(optionText)):
        x_position = randint(0,500)
        y_poition = randint(0,1700)*-1
        button = Button(x_position,y_poition,(80,80),optionText[i],color=Colors[i],bold=True, autofit=True)
        listOfButton.append(button)
    return listOfButton

def falling_animation(screen, buttons, dt):
    for button in buttons:
        if button.rect.top >= 600:
            del button
            continue
        direction = pygame.math.Vector2(0,1)
        speed = 200
        button.rect.center += speed*dt*direction
        button.draw(screen)
    
        
def draw_defeat(screen):
    screen.blit(defeat_img,defeat_rect)
    retry_button = Button(350,400,(100,80),"RETRY",(255, 182, 193),(245, 162, 173),True,autofit=True)
    retry_button.config(bold=True)
    retry_button.draw(screen)
    if retry_button.isClicked():
        return 'game'
    pygame.display.update()
    return 'defeat'

def draw_label(screen,question):
    label = Label(0,0,(450,40),question,(0,0,0),(177, 90, 255),('Arial',40),True,autofit=True)
    label.rect.center = (400,70)
    padding = 4 # padding in pixels
    rect = pygame.Rect(label.rect.left-padding,label.rect.top-padding, label.rect.width+(2*padding),label.rect.height+(2*padding))
    pygame.draw.rect(screen,(255,255,255),rect)
    label.draw(screen)

def draw_score(screen,score):
    gm_score = f'SCORE : {score}'
    font = pygame.font.SysFont('Arial',20,True,False) #Arial Bold font of size 20
    text_surf = font.render(gm_score,True,'white',wraplength= 0)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (5,5)
    screen.blit(text_surf,text_rect)

def menu_button():
    startButton = Button(300,250,(200,60),"START",(100,200,100),(50,255,50),hover=True,autofit=True)
    settingsButton = Button(300,350,(200,60),"SETTINGS",(100,200,250),(50,150,250),hover=True,autofit=True)
    quitButton = Button(300,450,(200,60),"QUIT",(250,100,100),(255,50,50), hover = True, autofit=True)
    return [startButton, settingsButton, quitButton]