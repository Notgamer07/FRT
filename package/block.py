import pygame

class Block:
    def __init__(self,x,y,dimension,text,color=None,text_color=(0,0,0),
                font=('Arial',40),bold=False,borderRadius=8, autofit = False):
        pygame.font.init()
        self.x = x
        self.y = y
        self.width, self.height = dimension
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.text = text
        self.fontType, self.fontSize = font
        self.textColor = text_color
        self.font = pygame.font.SysFont(self.fontType, self.fontSize)
        self.color = color
        self.autofit = autofit
        self.bold = bold 
        self.borderRadius = borderRadius

    def config(self,x=None,y=None,dimension=None,text=None,color=None,text_color=None,
               font=None,borderRadius=False, autofit = None, bold=None):
        if x is not None or y is not None:
            assert ( x is not None and y is not None), 'Only x-axis position value was given, Need both'
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, self.width, self.height)
        if dimension is not None: 
            assert (len(dimension) == 2), "Only Width value was give, Missing Height value also or Too many values was giveb"
            self.width, self.height = dimension
            self.rect = pygame.Rect(x, y, self.width, self.height)
        if text is not None:
            self.text = text
        if text_color is not None:
            self.textColor = text_color
        if font is not None:
           self.fontType, self.fontSize = font
           self.font = pygame.font.SysFont(self.fontType, self.fontSize, bold=bold)
        if (color is not None):
            self.color = color
        if borderRadius is not False:
            self.borderRadius = borderRadius
        if autofit is not None:
            self.autofit = autofit
        if bold is not None:
            self.bold = bold            
    
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
                    break
                font_size -= 1

            # Center and draw the text
            text_rect = text_surf.get_rect(center=self.rect.center)

        elif self.autofit == False:
            text_surf = self.font.render(self.text, True, self.textColor)
            text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    