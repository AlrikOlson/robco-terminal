import pygame


import random


class CRTEffect:

    def __init__(self, width, height):
        """
        Initializes the CRTEffect class.

        Args:
            width: The width of the screen.
            height: The height of the screen.
        """
        self.width = width
        self.height = height

    def apply_effect(self, overlay):
        """
        Applies a CRT screen effect to the overlay.

        Args:
            overlay: The overlay surface.
        """
        self._add_flickering_effect(overlay)

    def _add_flickering_effect(self, overlay):
        """
        Adds a flickering effect to the overlay.

        Args:
            overlay: The overlay surface.
        """
        flicker_intensity = random.randint(0, 5)  # Reduced intensity range
        flicker_surface = pygame.Surface((overlay.get_width(), overlay.get_height()), pygame.SRCALPHA)
        flicker_surface.fill((0, 255, 0, flicker_intensity))  # Fill with green color
        overlay.blit(flicker_surface, (0, 0))