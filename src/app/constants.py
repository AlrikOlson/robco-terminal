from src.assets.file_loader import FileLoader


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Fallout Font Path and Size
file_loader = FileLoader()
FONT_PATH = file_loader.get_path("src/assets/fonts/Perfect DOS VGA 437 Win.ttf")
FONT_SIZE = 20
