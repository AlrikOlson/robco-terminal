import pygame
from src.scenes.base_scene import BaseScene

class TextScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.USEREVENT:
            self._handle_state_transition()
            return False
        self.app.input_handler.handle_event(event)
        if self.app.input_handler.enter_pressed and not self.app.state_transition:
            self._handle_enter_pressed()
        return False

    def update(self):
        self.app.input_handler.update()

    def render(self):
        self.app.text_renderer.update()
        self.app.is_rendering = self.app.text_renderer.is_rendering()
        self.app.text_renderer.render()
        self._render_user_input()

    def enter(self):
        self.app.text_renderer.set_text(self.get_initial_text().copy())
        self.app.is_rendering = True
        self.app.state_transition = False

    def get_initial_text(self):
        raise NotImplementedError("Subclasses should implement this method")

    def _handle_enter_pressed(self):
        if self.app.is_rendering:
            self.app.text_renderer.finish_rendering()
            self.app.is_rendering = False
            self.app.input_handler.reset()
        elif self.app.input_handler.get_user_input():
            self._process_user_input()

    def _process_user_input(self):
        raise NotImplementedError("Subclasses should implement this method")

    def _render_user_input(self):
        user_input = self.app.input_handler.get_user_input()
        font = self.app.text_renderer.font
        y = 50 + len(self.app.text_renderer.get_text_buffer()) * self.app.text_renderer.line_height

        if user_input:
            user_input_surface = font.render(user_input, True, self.get_input_color())
            self.app.screen.blit(user_input_surface, (50, y))

    def get_input_color(self):
        raise NotImplementedError("Subclasses should implement this method")

    def _handle_state_transition(self):
        raise NotImplementedError("Subclasses should implement this method")
