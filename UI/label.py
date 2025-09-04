import pygame

class Label:
    def __init__(self, x, y, dimension, text,
                 color=(255,255,255), text_color=(0,0,0),
                 font=('Arial',40), bold=False,
                 customFontFilePath=None, customFontSize=40,
                 borderRadius=8, autofit=False):
        pygame.font.init()
        self.x, self.y = x, y
        self.width, self.height = dimension
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Style
        self.text = text
        self.color = color
        self.textColor = text_color
        self.fontType, self.fontSize = font
        self.bold = bold
        self.borderRadius = borderRadius
        self.autofit = autofit

        # Font setup
        if customFontFilePath:
            self.font = pygame.font.Font(customFontFilePath, customFontSize)
        else:
            self.font = pygame.font.SysFont(self.fontType, self.fontSize, bold=self.bold)

        # Pre-render once
        self._update_text_surface()

    def _update_text_surface(self):
        """(Re)calculate text surface, considering autofit."""
        if self.autofit:
            max_width = self.rect.width - 10
            max_height = self.rect.height - 10
            font_size = self.fontSize

            while font_size > 5:
                font = pygame.font.SysFont(self.fontType, font_size, bold=self.bold)
                text_surf = font.render(self.text, True, self.textColor)
                if text_surf.get_width() <= max_width and text_surf.get_height() <= max_height:
                    self.font = font
                    self.fontSize = font_size
                    break
                font_size -= 1

        self.text_surf = self.font.render(self.text, True, self.textColor)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def set_text(self, new_text):
        """Change label text and update surface"""
        self.text = new_text
        self._update_text_surface()

    def draw(self, screen):
        self.text_rect.center = self.rect.center
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.borderRadius)
        screen.blit(self.text_surf, self.text_rect)
