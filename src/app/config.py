from src.assets.file_loader import FileLoader


class Config:
    def __init__(self):
        file_loader = FileLoader()
        self.font_path = file_loader.get_path("assets/fonts/Perfect DOS VGA 437 Win.ttf")
        self.screen_width = 800
        self.screen_height = 600
        self.font_size = 20
        self.initial_scene = 'login_scene'
        self.password = "password123"
        self.standard_sound_files = [
            file_loader.get_path("assets/sounds/single_keypress_01.wav"),
            file_loader.get_path("assets/sounds/single_keypress_02.wav"),
            file_loader.get_path("assets/sounds/single_keypress_03.wav"),
            file_loader.get_path("assets/sounds/single_keypress_04.wav"),
            file_loader.get_path("assets/sounds/single_keypress_05.wav"),
            file_loader.get_path("assets/sounds/single_keypress_06.wav"),
            file_loader.get_path("assets/sounds/single_keypress_07.wav"),
            file_loader.get_path("assets/sounds/single_keypress_08.wav"),
        ]
        self.enter_sound_files = [
            file_loader.get_path("assets/sounds/enter_keypress_01.wav"),
            file_loader.get_path("assets/sounds/enter_keypress_02.wav"),
            file_loader.get_path("assets/sounds/enter_keypress_03.wav"),
        ]