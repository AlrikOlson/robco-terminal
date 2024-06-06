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
        self._draw_scanlines(overlay)
        self._add_flickering_effect(overlay)

    def _draw_scanlines(self, overlay):
        """
        Draws scanlines on the overlay.

        Args:
            overlay: The overlay surface.
        """
        scanline_color = (0, 0, 0, 50)  # Scanline color with transparency
        scanline_spacing = 3  # Spacing between scanlines
        for y in range(0, overlay.get_height(), scanline_spacing):
            pygame.draw.line(overlay, scanline_color, (0, y), (overlay.get_width(), y))

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