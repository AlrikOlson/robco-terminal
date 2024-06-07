# narrative_scene.py
import os
import pygame
from src.app.constants import GREEN
from src.scenes.menu_scene import MenuScene
from src.scenes.text_scene import TextScene

class NarrativeScene(MenuScene, TextScene):
    def __init__(self, app, chapter):
        MenuScene.__init__(self, app, chapter.get_options())
        TextScene.__init__(self, app)
        self.chapter = chapter

        # Check if API keys are set
        self.api_keys_set = (
            os.getenv("OPENAI_API_KEY") is not None and
            os.getenv("ANTHROPIC_API_KEY") is not None and
            os.getenv("NVIDIA_API_KEY") is not None
        )

    def enter(self):
        self.chapter.load_content()
        self.menu_options = self.chapter.get_options()
        self.app.text_renderer.set_text(self.chapter.get_text())
        self.app.is_rendering = True
        self.app.state_transition = False

    def handle_event(self, event):
        if self.chapter.conversational_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.app.text_renderer.scroll_up()
                elif event.key == pygame.K_DOWN:
                    self.app.text_renderer.scroll_down()
            return TextScene.handle_event(self, event)
        else:
            return MenuScene.handle_event(self, event)

    def update(self):
        if self.chapter.conversational_mode:
            TextScene.update(self)
        else:
            MenuScene.update(self)

    def render(self):
        if self.chapter.conversational_mode:
            self.app.text_renderer.enable_cursor()  # Enable cursor in conversational mode
            TextScene.render(self)
        else:
            self.app.text_renderer.disable_cursor()  # Disable cursor in menu mode
            MenuScene.render(self)

    def _process_menu_selection(self):
        selected_option = self.menu_options[self.selected_option]
        
        if selected_option == "[Exit]":
            if self.chapter.conversational_mode:
                self.chapter.conversational_mode = False  # Exit conversational mode
                self.chapter.conversation_histories.clear()  # Clear conversation history
            self.app.set_scene('success_scene')
        else:
            option_data = next((option for option in self.chapter.nodes[self.chapter.current_node]["options"] if option["text"] == selected_option), None)
            if option_data and option_data.get("conversational", False) and not self.api_keys_set:
                self.app.text_renderer.append_text("Conversational mode is disabled due to missing API keys.")
            else:
                self.chapter.process_selection(selected_option)
                self.menu_options = self.chapter.get_options()
                self.app.text_renderer.set_text(self.chapter.get_text())
                self.app.is_rendering = True
                self.selected_option = 0

    def _render_user_input(self):
        user_input = self.app.input_handler.get_user_input()
        self.app.text_renderer.set_user_input_text(user_input)
        font = self.app.text_renderer.font
        y = 50 + len(self.app.text_renderer.get_text_buffer()) * self.app.text_renderer.line_height

        if user_input:
            user_input_surface = font.render(user_input, True, self.get_input_color())
            self.app.screen.blit(user_input_surface, (50, y))

    def get_input_color(self):
        return GREEN

    def _handle_state_transition(self):
        if self.chapter.conversational_mode:
            self.chapter.conversational_mode = False  # Exit conversational mode
            self.app.set_scene('success_scene')
        else:
            self.app.set_scene('success_scene')

    def _process_user_input(self):
        user_input = self.app.input_handler.get_user_input()
        if user_input:
            self.chapter.process_selection(user_input)
            self.app.text_renderer.append_text("")
            self.app.text_renderer.append_text(self.chapter.get_text()[-2])
            self.app.text_renderer.append_text("")
            self.app.text_renderer.append_text(self.chapter.get_text()[-1])
            self.app.text_renderer.append_text("")
            self.app.input_handler.reset()
            self.app.text_renderer.scroll_to_bottom()
