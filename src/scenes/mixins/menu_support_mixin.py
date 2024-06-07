import pygame
from src.app.constants import GREEN

class MenuSupportMixin:
    def __init__(self):
        self.menu_options = []
        self.selected_option = 0

    def _render_menu(self, surface, text_renderer):
        self.text_renderer = text_renderer
        font = text_renderer.font
        if self.menu_options is None:
            print("menu_options is None")  # Debugging line
            return
        y_offset = 50 + len(text_renderer.get_text_buffer()) * 30
        padding = 10  # Increased padding for better visual
        border_thickness = 2  # Border thickness
        border_radius = 8   # Border radius

        for i, option in enumerate(self.menu_options):
            text = option
            option_surface = font.render(text, True, GREEN)
            
            # Get the dimensions of the text surface
            text_width, text_height = option_surface.get_size()
            
            # Create a new surface for the background rectangle
            bg_width = text_width + padding * 2
            bg_height = text_height + padding * 2
            bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            
            if i == self.selected_option:
                # Fill the background surface with the text color (green)
                bg_surface.fill(GREEN)
                
                # Render the text with transparent color
                text_surface = font.render(text, True, (0, 0, 0, 0))
                
                # Blit the text surface onto the background surface
                bg_surface.blit(text_surface, (padding, padding))
            else:
                # Render the text with normal text color (green)
                text_surface = font.render(text, True, GREEN)
                
                # Blit the text surface onto the background surface
                bg_surface.blit(text_surface, (padding, padding))
            
            # Blit the background surface onto the screen
            surface.blit(bg_surface, (50, y_offset))
            y_offset += bg_height

    def _draw_rounded_rect(self, surface, rect, color, thickness, radius):
        """
        Draw a rounded rectangle with specified corner radius.
        """
        pygame.draw.rect(surface, color, rect, thickness, border_radius=radius)

    def _handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self._process_menu_selection()

    def _process_menu_selection(self):
        if not self.text_renderer.is_rendering():
            selected_option = self.menu_options[self.selected_option]
        return selected_option
