import pygame
from .button import Button  # Adjust this import if needed

class RaisedButton(Button):
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        is_hovered = self.rect.collidepoint(mouse_pos)
        is_pressed = is_hovered and mouse_pressed

        # Determine base color
        bg_color = self.hoverColor if self.hover and is_hovered else self.color

        # Shadow and highlight colors
        shadow_offset = 4 if not is_pressed else 1
        highlight_color = (min(bg_color[0]+40, 255), min(bg_color[1]+40, 255), min(bg_color[2]+40, 255))
        shadow_color = (max(bg_color[0]-60, 0), max(bg_color[1]-60, 0), max(bg_color[2]-60, 0))

        # Shadow (bottom-right)
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=self.borderRadius)

        # Highlight (top-left)
        highlight_rect = self.rect.move(-1, -1)
        pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=self.borderRadius)

        # Actual button (slightly pressed if clicked)
        button_rect = self.rect.move(1, 1) if is_pressed else self.rect
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=self.borderRadius)

        # Draw text
        if self.autofit:
            max_width = self.rect.width - 10
            max_height = self.rect.height - 10
            font_size = self.fontSize
            while font_size > 5:
                font = pygame.font.SysFont(self.fontType, font_size, bold=self.bold)
                text_surf = font.render(self.text, True, self.textColor)
                if text_surf.get_width() <= max_width and text_surf.get_height() <= max_height:
                    break
                font_size -= 1
            text_rect = text_surf.get_frect(center=button_rect.center)
        else:
            text_surf = self.font.render(self.text, True, self.textColor)
            text_rect = text_surf.get_frect(center=button_rect.center)

        screen.blit(text_surf, text_rect)
