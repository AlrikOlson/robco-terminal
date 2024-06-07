from src.rendering.opengl_initializer import OpenGLInitializer
from src.rendering.renderer import Renderer
from src.rendering.shader_factory import ShaderFactory
from src.rendering.texture_manager import TextureManager


import pygame


class TerminalScreen:
    """
    A class to represent and render a terminal screen with CRT-like effects using Pygame and OpenGL.
    """

    def __init__(self, width, height, background_color):
        """
        Initializes the TerminalScreen.

        Args:
            width: The width of the screen.
            height: The height of the screen.
            background_color: The background color of the screen.
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        self.screen = None
        self.overlay = None
        self.curvature_shader = None
        self.opengl_init = OpenGLInitializer()

    def initialize(self):
        """
        Initializes Pygame and OpenGL, and creates the curvature shader.
        """
        self._initialize_pygame()
        self.opengl_init.initialize()
        self.curvature_shader = ShaderFactory.create_curvature_shader()

    def display(self, current_time):
        """
        Displays the screen with CRT effects applied and renders it.
        """
        surface = pygame.Surface(
            (self.overlay.get_width(), self.overlay.get_height()), pygame.SRCALPHA
        )
        self.overlay.blit(surface, (0, 0))
        texture_id = TextureManager.create_texture_id(self.overlay)
        TextureManager.bind_texture(texture_id, self.curvature_shader)
        Renderer.render_texture(self.curvature_shader, current_time, self.width, self.height)
        pygame.display.flip()
        TextureManager.cleanup(texture_id)

    def clear(self):
        """
        Clears the overlay.
        """
        self.overlay.fill((0, 0, 0, 0))  # Clear overlay

    def blit(self, source, dest):
        """
        Blits a source surface onto the overlay at the given destination.

        Args:
            source: The source surface to be blitted.
            dest: The destination coordinates on the overlay as a tuple.
        """
        self.overlay.blit(source, dest)

    def _initialize_pygame(self):
        """
        Initializes Pygame and sets up the display window.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF
        )
        pygame.display.set_caption("ROBCO Industries (TM) Termlink")
        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
