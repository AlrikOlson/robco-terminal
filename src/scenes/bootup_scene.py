import pygame
from src.scenes.base_scene import BaseScene

class BootupScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.bootup_text_lines = [
            "Initializing boot sequence...",
            "Loading system files...",
            "Checking hardware components...",
            "Initializing RobCo Industries Termlink...",
            "Welcome to RobCo Industries(TM) Termlink",
            "",
            "System Ready"
        ]
        self.current_line_index = 0
        self.last_update_time = 0
        self.line_delay = 1.0  # Delay between lines in seconds

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return True
        # Ignore Enter key press during boot-up
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return False
        return False

    def update(self):
        current_time = pygame.time.get_ticks() / 1000.0  # Get time in seconds
        if current_time - self.last_update_time >= self.line_delay:
            self.last_update_time = current_time
            if self.current_line_index < len(self.bootup_text_lines):
                self.app.text_renderer.append_text(self.bootup_text_lines[self.current_line_index])
                self.current_line_index += 1
            else:
                self.app.state_transition = True

        if self.app.state_transition:
            self.app.set_scene('login_scene')

    def render(self):
        self.app.text_renderer.update()
        self.app.is_rendering = self.app.text_renderer.is_rendering()
        self.app.text_renderer.render()

    def enter(self):
        self.app.text_renderer.set_text([])
        self.app.is_rendering = True
        self.app.state_transition = False
        self.current_line_index = 0
        self.last_update_time = pygame.time.get_ticks() / 1000.0