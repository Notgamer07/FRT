import pygame

class Label:
    def __init__(self,x,y,dimension,text,color=(255,255,255),
                 text_color=(0,0,0),font=('Arial',40),bold=False,
                 customFontFilePath=False,customFontSize=40,borderRadius=8, 
                 autofit = False):
        pygame.font.init()
        self.x = x
        self.y = y
        self.width, self.height = dimension
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.text = text
        self.fontType, self.fontSize = font
        self.textColor = text_color
        self.font = pygame.font.SysFont(self.fontType, self.fontSize)
        self.borderRadius = borderRadius
        self.autofit = autofit
        self.bold = bold
        self.color = color
        if customFontFilePath is not False:
            self.font = pygame.font.Font(customFontFilePath,customFontSize)
    
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect,border_radius=self.borderRadius)
        if self.autofit:
            # Dynamically scale font to fit
            max_width = self.rect.width - 10  # 5px padding on each side
            max_height = self.rect.height - 10
            font_size = self.fontSize

            # Try decreasing font size until it fits
            while font_size > 5:
                font = pygame.font.SysFont(self.fontType, font_size,bold=self.bold)
                text_surf = font.render(self.text, True, self.textColor)
                if text_surf.get_width() <= max_width and text_surf.get_height() <= max_height:
                    self.fontSize = font_size
                    break
                font_size -= 1

            # Center and draw the text
            text_rect = text_surf.get_rect(center=self.rect.center)

        elif self.autofit == False:
            text_surf = self.font.render(self.text, True, self.textColor)
            text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        screen.fill('orange')
        label = Label(200,200,(100,80),"IT WORKED",(234,90,90),(255,255,255) ,bold= True, autofit=True)
        label.draw(screen)
        pygame.display.update()
        