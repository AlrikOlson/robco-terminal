import pygame
from src.app.constants import GREEN
from src.scenes.text_scene import TextScene

class LoginScene(TextScene):
    def __init__(self, app, password):
        super().__init__(app)
        self.initial_text = [
            "Welcome to ROBCO Industries(TM) Termlink",
            "Password Required",
            "",
            "Attempts Remaining: 4",
            "",
            "Enter Password Now"
        ]
        self.password = password
        self.attempts_remaining = 4
        self.terminal_locked = False

    def get_initial_text(self):
        return self.initial_text

    def get_input_color(self):
        return GREEN

    def _process_user_input(self):
        if self.terminal_locked:
            return

        user_input = self.app.input_handler.get_user_input()
        if self._is_password_correct(user_input):
            self.app.text_renderer.append_text("Access Granted")
            self.app.state_transition = True
            pygame.time.set_timer(pygame.USEREVENT, 100)
        else:
            self._handle_wrong_password()

        self.app.input_handler.reset()

    # Check if the user input matches the password
    def _is_password_correct(self, user_input):
        return user_input == self.password

    def _handle_wrong_password(self):
        self.attempts_remaining -= 1
        self.app.text_renderer.append_text("Access Denied")
        self._update_attempts_remaining()
        if self.attempts_remaining == 0:
            self.app.text_renderer.append_text("Terminal Locked")
            self.terminal_locked = True

    def _update_attempts_remaining(self):
        full_text_lines = self.app.text_renderer.full_text_lines
        if len(full_text_lines) > 3:
            full_text_lines[3] = f"Attempts Remaining: {self.attempts_remaining}"
            self.app.text_renderer.set_text(full_text_lines)

    def _handle_state_transition(self):
        pygame.time.set_timer(pygame.USEREVENT, 0)
        self.reset_attempts()
        self.app.set_scene('success_scene')

    def reset_attempts(self):
        self.attempts_remaining = 4
        self.terminal_locked = False

    # Display the concealed input (asterisks) instead of actual characters
    def _render_user_input(self):
        user_input = self.app.input_handler.get_user_input()
        concealed_input = "*" * len(user_input)  # Replace characters with asterisks
        self.app.text_renderer.set_user_input_text(concealed_input)
        font = self.app.text_renderer.font
        y = 50 + len(self.app.text_renderer.get_text_buffer()) * self.app.text_renderer.line_height

        if concealed_input:
            user_input_surface = font.render(concealed_input, True, self.get_input_color())
            self.app.screen.blit(user_input_surface, (50, y))

    def _handle_enter_pressed(self):
        if self.app.is_rendering:
            self.app.text_renderer.finish_rendering()
            self.app.is_rendering = False
        else:
            user_input = self.app.input_handler.get_user_input()
            if user_input:
                self._process_user_input()
