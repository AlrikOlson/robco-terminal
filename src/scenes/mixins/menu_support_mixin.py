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
            if i == self.selected_option:
                # Render with normal text color (green) and draw border around
                text_color = GREEN
                border_color = GREEN
            else:
                # Render with normal text color (green) and no border
                text_color = GREEN
                border_color = None
            
            text = "> " + option if i == self.selected_option else "  " + option
            option_surface = font.render(text, True, text_color)
            
            # Draw border rectangle if selected
            rect = option_surface.get_rect(topleft=(50, y_offset))
            if border_color:
                self._draw_rounded_rect(surface, rect.inflate(padding, padding), border_color, border_thickness, border_radius)
            
            # Blit the text onto the screen
            surface.blit(option_surface, rect.topleft)
            y_offset += 30

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
