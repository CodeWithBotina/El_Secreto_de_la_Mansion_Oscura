"""
Button UI component
"""
import pygame
from ..game.game_constants import WHITE, BLACK

class Button:
    def __init__(self, x, y, width, height, text="", action=None, color=WHITE, image=None):
        """
        Initialize button
        
        Args:
            x (int): X position
            y (int): Y position
            width (int): Button width
            height (int): Button height
            text (str): Button text
            action (callable): Function to call when clicked
            color (tuple): RGB color tuple
            image (Surface): Optional image for the button
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.hover_color = (200, 200, 200)
        self.is_hovered = False
        self.image = image

    def draw(self, screen):
        """Draw button on screen"""
        color = self.hover_color if self.is_hovered else self.color
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, color, self.rect)
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and self.action:
                self.action()
