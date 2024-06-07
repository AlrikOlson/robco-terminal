import pygame
from src.scenes.menu_scene import MenuScene

class PowerManagementScene(MenuScene):
    def __init__(self, app):
        super().__init__(app, ["Reactor Status", "Power Allocation", "Emergency Shutdown", "Back to Main Menu"])

    def enter(self):
        new_text = [
            "POWER MANAGEMENT",
            "----------------",
            "Please select a power management option:",
            ""
        ]
        self.app.text_renderer.set_text(new_text)
        self.app.is_rendering = True
        self.app.state_transition = False

    def _process_menu_selection(self):
        selected_option = self.menu_options[self.selected_option]
        if selected_option == "Reactor Status":
            self.app.text_renderer.append_text("Reactor Status: Nominal.")
            self.app.state_transition = True
        elif selected_option == "Power Allocation":
            self.app.text_renderer.append_text("Opening Power Allocation Menu...")
            self.app.state_transition = True
        elif selected_option == "Emergency Shutdown":
            self.app.text_renderer.append_text("Initiating Emergency Shutdown...")
            self.app.state_transition = True
        elif selected_option == "Back to Main Menu":
            self.app.set_scene('success_scene')
        return False

    def _handle_state_transition(self):
        if self.app.state_transition:
            self.app.text_renderer.finish_rendering()
            self.app.set_scene('success_scene')
