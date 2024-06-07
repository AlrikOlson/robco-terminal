import pygame
from src.scenes.menu_scene import MenuScene

class SuccessScene(MenuScene):
    def __init__(self, app):
        super().__init__(app, ["Vault Overseer Log", "Research Log", "Business Terminal", "Log out", "Quit"])

    def enter(self):
        new_text = [
            "Welcome to the Vault-Tec terminal.",
            "System Status: All systems functional.",
            ""
        ]
        self.app.text_renderer.set_text(new_text)
        self.app.is_rendering = True
        self.app.state_transition = False

    def _process_menu_selection(self):
        selected_option = self.menu_options[self.selected_option]
        if selected_option == "Vault Overseer Log":
            self.app.set_scene('vault_overseer')
        elif selected_option == "Research Log":
            self.app.set_scene('research_log')
        elif selected_option == "Business Terminal":
            self.app.set_scene('business_terminal')
        elif selected_option == "Log out":
            self.app.set_scene('login_scene')
        elif selected_option == "Quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        return False