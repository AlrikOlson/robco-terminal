import pygame

from src.scenes.menu_scene import MenuScene


class SuccessScene(MenuScene):
    def __init__(self, app):
        super().__init__(app, [
            "DATA LOGS",
            "PERSONNEL RECORDS",
            "SECURITY CONTROLS",
            "POWER MANAGEMENT",
            "VAULT MAP",
            "LOG OUT",
            "QUIT"
        ])

    def enter(self):
        new_text = [
            "WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK",
            "VAULT CONTROL SYSTEM - VT-CLI 0.9",
            "",
            "COPYRIGHT 2075 ROBCO INDUSTRIES",
            "-SERVER 6-",
            ""
        ]
        self.app.text_renderer.set_text(new_text)
        self.app.is_rendering = True
        self.app.state_transition = False

    def _process_menu_selection(self):
        selected_option = self.menu_options[self.selected_option]
        if selected_option == "DATA LOGS":
            self.app.set_scene('data_logs')
        elif selected_option == "PERSONNEL RECORDS":
            self.app.set_scene('personnel_records')
        elif selected_option == "SECURITY CONTROLS":
            self.app.set_scene('security_controls')
        elif selected_option == "POWER MANAGEMENT":
            self.app.set_scene('power_management')
        elif selected_option == "VAULT MAP":
            self.app.set_scene('vault_scene')
        elif selected_option == "LOG OUT":
            self.app.set_scene('login_scene')
        elif selected_option == "QUIT":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        return False
