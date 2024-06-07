import pygame
from src.scenes.base_scene import BaseScene
from src.scenes.mixins.menu_support_mixin import MenuSupportMixin

class MenuScene(BaseScene, MenuSupportMixin):
    def __init__(self, app, menu_options):
        super().__init__(app)
        MenuSupportMixin.__init__(self)
        self.input_mode = "menu"
        self.menu_options = menu_options

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return True

        if self.input_mode == "menu":
            if not self.app.is_rendering:  # Check if rendering is complete before handling menu events
                self._handle_menu_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return True
            elif event.key == pygame.K_l:
                self.app.set_scene('login_scene')
            elif event.key == pygame.K_RETURN and not self.app.state_transition:
                self.app.text_renderer.finish_rendering()
                self.app.is_rendering = False

        return False

    def update(self):
        pass

    def render(self):
        self.app.text_renderer.disable_cursor()  # Disable cursor when rendering menu
        self.app.text_renderer.update()
        self.app.is_rendering = self.app.text_renderer.is_rendering()
        self.app.text_renderer.render()
        if self.input_mode == "menu" and not self.app.is_rendering:  # Only render the menu if rendering is complete
            self._render_menu(self.app.screen.overlay, self.app.text_renderer)  # Pass overlay
        else:
            self.app.text_renderer.enable_cursor()  # Enable cursor when not in menu mode

    def _process_menu_selection(self):
        raise NotImplementedError("Subclasses should implement this method")
