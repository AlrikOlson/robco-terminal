import pygame
from src.scenes.menu_scene import MenuScene

class DataLogsScene(MenuScene):
    def __init__(self, app):
        super().__init__(app, ["Medical Terminal", "Security Terminal", "Overseer Terminal", "Back to Main Menu"])

    def enter(self):
        new_text = [
            "DATA LOGS",
            "---------",
            "Please select a data log to view:",
            ""
        ]
        self.app.text_renderer.set_text(new_text)
        self.app.is_rendering = True
        self.app.state_transition = False

    def _process_menu_selection(self):
        selected_option = self.menu_options[self.selected_option]
        if selected_option == "Medical Terminal":
            self.app.set_scene('vault149_medical_terminal')
        elif selected_option == "Security Terminal":
            self.app.set_scene('vault149_security_terminal')
        elif selected_option == "Overseer Terminal":
            self.app.set_scene('vault149_overseer_terminal')
        elif selected_option == "Back to Main Menu":
            self.app.set_scene('success_scene')
        return False
