import pygame

class FontLoader:
    def load(self, font_path, font_size):
        raise NotImplementedError("Subclasses should implement this method")

class FileFontLoader(FontLoader):
    def __init__(self, font_path, font_size):
        self.font_path = font_path
        self.font_size = font_size

    def load(self):
        try:
            return pygame.font.Font(self.font_path, self.font_size)
        except FileNotFoundError:
            raise FileNotFoundError(f"Font file not found at path: {self.font_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load font: {e}")
