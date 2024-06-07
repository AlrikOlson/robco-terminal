import pygame
from src.scenes.menu_scene import MenuScene

class SecurityControlsScene(MenuScene):
    def __init__(self, app):
        super().__init__(app, ["Lockdown", "Override", "Surveillance", "Back to Main Menu"])

    def enter(self):
        new_text = [
            "SECURITY CONTROLS",
            "-----------------",
            "Please select a security control option:",
            ""
        ]
        self.app.text_renderer.set_text(new_text)
        self.app.is_rendering = True
        self.app.state_transition = False

    def _process_menu_selection(self):
        selected_option = self.menu_options[self.selected_option]
        if selected_option == "Lockdown":
            self.app.text_renderer.append_text("Initiating Lockdown Protocol...")
            self.app.state_transition = True
        elif selected_option == "Override":
            self.app.text_renderer.append_text("Override Command Executed...")
            self.app.state_transition = True
        elif selected_option == "Surveillance":
            self.app.text_renderer.append_text("Accessing Surveillance Cameras...")
            self.app.state_transition = True
        elif selected_option == "Back to Main Menu":
            self.app.set_scene('success_scene')
        return False

    def _handle_state_transition(self):
        if self.app.state_transition:
            self.app.text_renderer.finish_rendering()
            self.app.set_scene('success_scene')
