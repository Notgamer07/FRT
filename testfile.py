import pygame
from UI import Block,RaisedButton, Label
from random import randint, choice
import json
import os


"""  PLayer """
class Player(pygame.sprite.Sprite):
    def __init__(self, size: tuple, color=(255, 255, 255), speed=400):
        super().__init__()
        self.Color = color
        self.Speed = speed
        self.Direction = pygame.math.Vector2(0, 0)

        # make rect, position it at bottom-center
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = (WIDTH // 2, HEIGHT - (size[1] // 2) - 4)

        # store position (only care about x for smooth movement)
        self.Position = pygame.math.Vector2(self.rect.centerx, 0)

    def changeDirection(self, x):
        self.Direction.x = x

    def draw(self, surface,dt):
        self.Position.x += self.Direction.x * self.Speed * dt
        self.rect.centerx = round(self.Position.x)
        pygame.draw.rect(surface, self.Color, self.rect, border_radius=8)



COLOR= [(255, 87, 87), (177, 90, 255), (50, 205, 50), (255, 223, 0), (255, 20, 147)]

with open("data1.json", "r") as f:
    data = json.load(f)

# Iterator over levels
level_iter = iter(data)
current_level = next(level_iter)
question_iter = iter(current_level["questions"])

#This will create the menu buttons and return them in a list of buttons
def menu_button()->list[RaisedButton]:
    startButton = RaisedButton(300,250,(200,60),"START",(100,200,100),(50,255,50),hover=True,autofit=True, bold=True)
    settingsButton = RaisedButton(300,350,(200,60),"SETTINGS",(100,200,250),(50,150,250),hover=True,autofit=True)
    quitButton = RaisedButton(300,450,(200,60),"QUIT",(250,100,100),(255,50,50), hover = True, autofit=True)
    return [startButton, settingsButton, quitButton]

def draw_score(screen,score):
    gm_score = f'SCORE : {score}'
    font = pygame.font.SysFont('Arial',20,True,False) #Arial Bold font of size 20
    text_surf = font.render(gm_score,True,'white',wraplength= 0)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (5,5)
    screen.blit(text_surf,text_rect)

def draw_heart(lifes):
    for i in range(lifes):
        health_rect.center = (WIDTH-50-i*22, 20)
        screen.blit(health, health_rect)

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

def next_question():
    '''To use this function, call this function
    in 'ques' like ques = next_question() and change 
    displayQuestion variable too!! like displayQuestion = ques['question']'''
    global current_level, question_iter, level_iter

    try:
        return next(question_iter)  # get next question from current level
    except StopIteration:
        # If current level is exhausted, go to next level
        try:
            current_level = next(level_iter)
            question_iter = iter(current_level["questions"])
            return next(question_iter)
        except StopIteration:
            return None  # no more questions at all

def draw_background(screen):
    for i in range(20):
        screen.blit(star_frames[frame_no[i]],star_pos[i])


ques = next_question()
DisplayQuestion = ques['question']
label = Label(
        0, 0, (450, 40), DisplayQuestion,
        color=(0,0,0), text_color=(177, 90, 255),
        font=('Arial', 40), bold=True,
        autofit=True
    )
label.rect.center = (400,70)


def spawn_block(group: pygame.sprite.Group):
    global ques
    options = ques['options']
    x_pos = randint(0, WIDTH - 80)
    b = Block(x_pos, -80, (80, 80), text=choice(options), color=COLOR[randint(0,len(COLOR)-1)], bold=True)
    group.add(b)


pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sound Button Test")

health = pygame.image.load(os.path.join(os.path.curdir, "img", "red-heart.png")).convert_alpha()
health_rect = health.get_rect()
lifes = 3

start_timer = pygame.time.get_ticks()
clock = pygame.time.Clock()

cooldownTimer = 1200
block_spawn_time = 0

all_blocks = pygame.sprite.Group()
speed_of_block = 200

timer_for_speed = 2000
time_changed = 0

current_screen = "Menu"

# --- Loading Star img for the background ---
star_img = pygame.image.load(os.path.join(os.path.dirname(__file__),'img','star.png')).convert_alpha()
star_frames = [] #contains section of star image, 4 frame of star from brigth to dim
frame_width = 32 # width of each frame of star img
# Stores the four section of star img into star_frames list
for i in range(4): 
    star_rect = pygame.Rect(i*frame_width, 0, frame_width, 32)
    surf = star_img.subsurface(star_rect).copy()
    star_frames.append(surf)
frame_no=[] # Stores the total number of stars. change for loop (20) to change number of star
for _ in range(20):
    ran = randint(0,3)
    frame_no.append(ran)
star_pos  = [] # stores (x,y) position for each star in frame_no
for _ in range(20):
    x = randint(0,800)
    y = randint(0,600)
    star_pos.append((x,y))

player = Player((90,20))
score = 0

run = True
while run:
    globalTimer = pygame.time.get_ticks()
    dt = clock.tick(60)/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pass
    #--------------------- Menu -------------------------
    if current_screen == "Menu":
        menuButtons = menu_button()

        for i,button in enumerate(menuButtons):
            button.draw(screen)
            if button.isClicked():
                if i == 0:
                    current_screen = "Game"
                elif i == 1:
                    current_screen = "Settings"
                else:
                    run = False
        
    #---------------------- Game ------------------------
    if current_screen == "Game":
        if (globalTimer - block_spawn_time) >= cooldownTimer:
            block_spawn_time = pygame.time.get_ticks()
            spawn_block(all_blocks)
        
        # if(globalTimer - time_changed)>=timer_for_speed:
        #     time_changed = pygame.time.get_ticks()
        #     speed_of_block += 50
        
        
        #Collisions
        collidedBlock = pygame.sprite.spritecollideany(player,all_blocks)
        if collidedBlock is not None:
            correctAnswer = ques["correct_answer"]
            if collidedBlock.text == correctAnswer:
                score += 1
                ques = next_question()
                DisplayQuestion = ques['question']
                label.set_text(DisplayQuestion)
                if ques is None:
                    current_screen = "victory"
                    print("victory screen")
            else:
                if(lifes -1 == 0):
                    current_screen = "defeat"
                    print("defeat screen")
                    continue
                lifes -= 1
            all_blocks.remove(collidedBlock)


        #Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.left > 0: #Pressing Left and player isn't out of bounds of left screen
            player.changeDirection(-1)
        elif keys[pygame.K_RIGHT] and player.rect.right < WIDTH: #Pressing Right and player isn't out of right screen
            player.changeDirection(1)
        elif player.rect.left <= 0 or player.rect.right >= WIDTH:
            player.Direction.x *= -1
            

        #Displaying on Screen 
        screen.fill((0,0,0)) #Painting Whole Screen Black
        draw_background(screen) # Adding stars
        all_blocks.update(dt, speed_of_block) 
        all_blocks.draw(screen) # Adding all the blocks
        player.draw(screen,dt) # Adding Player 
        label.draw(screen) # Adding Question Label
        draw_heart(lifes) # Adding Hearts
        draw_score(screen, score)
        # Removes all the Block that fall out screen
        for block in all_blocks.copy(): 
            if block.rect.top > HEIGHT:
                all_blocks.remove(block)


    # Flip display
    pygame.display.flip()
    
pygame.quit()