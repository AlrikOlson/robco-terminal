import pygame
from src.scenes.menu_scene import MenuScene

class ViewAllPersonnelScene(MenuScene):
    def __init__(self, app):
        personnel_records = [
            "John Doe - Engineering",
            "Jane Smith - Medical",
            "Robert Johnson - Security",
            # Add more personnel records as needed
        ]
        # Add an option to go back to the previous menu
        personnel_records.append("BACK TO PERSONNEL RECORDS MENU")
        super().__init__(app, personnel_records)

    def enter(self):
        new_text = [
            "PERSONNEL RECORDS - VIEW ALL PERSONNEL",
            "--------------------------------------",
            "Select a personnel record to view details:",
            ""
        ]
        self.app.text_renderer.set_text(new_text)
        self.app.is_rendering = True
        self.app.state_transition = False

    def _process_menu_selection(self):
        selected_option = self.menu_options[self.selected_option]
        if selected_option == "BACK TO PERSONNEL RECORDS MENU":
            self.app.set_scene('personnel_records')
        else:
            self.app.text_renderer.append_text(selected_option)
