import time
import pygame

class InputHandler:
    def handle_event(self, event):
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_user_input(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def update(self):
        raise NotImplementedError("Subclasses should implement this method")

    def reset(self):
        raise NotImplementedError("Subclasses should implement this method")

class TerminalInputHandler(InputHandler):
    def __init__(self, initial_delay=0.3, repeat_interval=0.03):
        self.user_input = ""
        self.enter_pressed = False
        self.backspace_pressed = False
        self.last_backspace_time = 0
        self.initial_delay = initial_delay
        self.repeat_interval = repeat_interval
        self.backspace_start_time = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event)
        elif event.type == pygame.KEYUP:
            self._handle_keyup(event)
        return self.user_input

    def _handle_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self._handle_backspace()
        elif event.key == pygame.K_RETURN:
            self.enter_pressed = True
        else:
            self.user_input += event.unicode

    def _handle_keyup(self, event):
        if event.key == pygame.K_RETURN:
            self.enter_pressed = False
        if event.key == pygame.K_BACKSPACE:
            self.backspace_pressed = False

    def _handle_backspace(self):
        if not self.backspace_pressed:
            self.backspace_pressed = True
            self.backspace_start_time = time.time()
        self.last_backspace_time = time.time()
        self.user_input = self.user_input[:-1]

    def update(self):
        if self.backspace_pressed:
            self._perform_repeated_backspace()

    def _perform_repeated_backspace(self):
        current_time = time.time()
        if (current_time - self.backspace_start_time >= self.initial_delay) and \
           (current_time - self.last_backspace_time >= self.repeat_interval):
            self.user_input = self.user_input[:-1]
            self.last_backspace_time = current_time

    def get_user_input(self):
        return self.user_input

    def reset(self):
        self.user_input = ""
        self.enter_pressed = False
        self.backspace_pressed = False
        self.last_backspace_time = 0
        self.backspace_start_time = 0
