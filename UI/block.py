import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, size, text,
                 color=(200, 200, 200), text_color=(0, 0, 0),
                 font_name='Arial', bold=False):
        super().__init__()
        pygame.font.init()

        # Use FRect instead of Rect
        self.rect = pygame.FRect(x, y, *size)  # FRect stores floats
        # No need for separate pos_y anymore
        # self.pos_y = float(y)  <-- remove

        # Block attributes
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font_name = font_name
        self.bold = bold

        # Pre-render text surface
        self._text_surf = None
        self._font_size = None
        self._needs_update = True

        # Create image surface for the sprite
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self._render_text()

    def _render_text(self):
        if not self._needs_update:
            return

        max_width = self.rect.width - 20
        max_height = self.rect.height - 20
        font_size = int(min(max_width, max_height))

        while font_size > 5:
            font = pygame.font.SysFont(self.font_name,font_size, bold=self.bold)
            text_surf = font.render(self.text, True, self.text_color)
            if text_surf.get_width() <= max_width and text_surf.get_height() <= max_height:
                self._text_surf = text_surf
                self._font_size = font_size
                break
            font_size -= 1

        if not self._text_surf:
            self._text_surf = pygame.font.SysFont(self.font_name, 10).render(self.text, True, self.text_color)

        self._needs_update = False
        self._redraw_image()

    def _redraw_image(self):
        """Redraw block rectangle + text onto self.image"""
        self.image.fill((0, 0, 0, 0))  # clear with transparency
        pygame.draw.rect(self.image, self.color,
                         self.image.get_rect(), border_radius=8)

        # center text
        text_rect = self._text_surf.get_rect(center=self.image.get_rect().center)
        self.image.blit(self._text_surf, text_rect)

    def fall(self, dy):
        """Update FRect position"""
        self.rect.y += dy  # FRect handles floats automatically

    def update(self, dt, speed):
        """Standard sprite update method"""
        self.fall(speed * dt)
