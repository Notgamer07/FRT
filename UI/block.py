import pygame

class Block:
    def __init__(self, x, y, size, text, color=(200, 200, 200), text_color=(0, 0, 0), font_name='Arial', bold=False):
        pygame.font.init()
        self.rect = pygame.Rect(x, y, *size)  # size = (width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font_name = font_name
        self.bold = bold
        self._text_surf = None
        self._text_rect = None
        self._font_size = None
        self._needs_update = True  # Mark when we need to re-render

    def _render_text(self):
        """Generate the font surface only when needed (with autofit + padding)."""
        if not self._needs_update:
            return

        max_width = self.rect.width - 20  # 10px horizontal padding both sides
        max_height = self.rect.height - 20  # 10px vertical padding both sides
        font_size = min(max_width, max_height)

        while font_size > 5:
            font = pygame.font.SysFont(self.font_name, font_size, bold=self.bold)
            text_surf = font.render(self.text, True, self.text_color)
            if text_surf.get_width() <= max_width and text_surf.get_height() <= max_height:
                self._text_surf = text_surf
                self._text_rect = text_surf.get_rect(center=self.rect.center)
                self._font_size = font_size
                self._needs_update = False
                return
            font_size -= 1

        # fallback
        self._text_surf = pygame.font.SysFont(self.font_name, 10).render(self.text, True, self.text_color)
        self._text_rect = self._text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        self._render_text()
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        screen.blit(self._text_surf, self._text_rect)

    def move(self, dx=0, dy=0):
        """Move block and update text position"""
        self.rect.move_ip(dx, dy)
        if self._text_rect:
            self._text_rect.move_ip(dx, dy)

    # def set_pos(self, x, y):
    #     """Set position and mark text for re-alignment"""
    #     self.rect.topleft = (x, y)
    #     self._needs_update = True
