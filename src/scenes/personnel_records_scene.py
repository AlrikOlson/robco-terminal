import pygame
from src.scenes.menu_scene import MenuScene

class PersonnelRecordsScene(MenuScene):
    def __init__(self, app):
        super().__init__(app, ["View All Personnel", "Search by Name", "Back to Main Menu"])

    def enter(self):
        new_text = [
            "PERSONNEL RECORDS",
            "-----------------",
            "Please select an option:",
            ""
        ]
        self.app.text_renderer.set_text(new_text)
        self.app.is_rendering = True
        self.app.state_transition = False

    def _process_menu_selection(self):
        selected_option = self.menu_options[self.selected_option]
        if selected_option == "View All Personnel":
            self.app.set_scene('view_all_personnel')
        elif selected_option == "Search by Name":
            self.app.set_scene('search_personnel')
        elif selected_option == "Back to Main Menu":
            self.app.set_scene('success_scene')
        return False
