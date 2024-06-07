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

        terminal_width = surface.get_width()  # Get full width of the terminal
        y_offset = 50 + len(text_renderer.get_text_buffer()) * 30
        padding = 10  # Padding around text

        left_margin = text_renderer.margin[0]  # Use the left margin from text_renderer

        for i, option in enumerate(self.menu_options):
            text = option
            option_surface = font.render(text, True, GREEN)

            # Create a new surface for the background rectangle
            text_width, text_height = option_surface.get_size()
            bg_surface = pygame.Surface((terminal_width, text_height + padding * 2), pygame.SRCALPHA)

            if i == self.selected_option:
                bg_surface.fill(GREEN)
                text_surface = font.render(text, True, (0, 0, 0))  # Render text in black for contrast
            else:
                text_surface = font.render(text, True, GREEN)

            text_x = left_margin + padding  # Ensure the text aligns with the left margin of the existing content
            text_y = padding  # Vertical padding at the top

            bg_surface.blit(text_surface, (text_x, text_y))
            surface.blit(bg_surface, (0, y_offset))  # Ensure background spans full width
            y_offset += bg_surface.get_height()

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
