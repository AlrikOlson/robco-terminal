import pygame
from src.scenes.text_scene import TextScene

class SearchPersonnelScene(TextScene):
    def __init__(self, app):
        super().__init__(app)
        self.search_result = ""

    def get_initial_text(self):
        return [
            "PERSONNEL RECORDS - SEARCH BY NAME",
            "-----------------------------------",
            "Enter name to search:",
        ]

    def _process_user_input(self):
        search_query = self.app.input_handler.get_user_input()
        self.search_result = self.search_personnel_by_name(search_query)
        self.app.text_renderer.append_text(self.search_result)
        self.app.input_handler.reset()

    def search_personnel_by_name(self, name):
        personnel_records = {
            "John Doe": "John Doe - Engineering",
            "Jane Smith": "Jane Smith - Medical",
            "Robert Johnson": "Robert Johnson - Security",
            # Add more personnel records as needed
        }
        return personnel_records.get(name, "Personnel not found")

    def _handle_state_transition(self):
        self.app.set_scene('personnel_records')

    def get_input_color(self):
        return (255, 255, 255)
