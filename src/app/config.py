class Config:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.font_path = "src/assets/fonts/Perfect DOS VGA 437 Win.ttf"
        self.font_size = 20
        self.initial_scene = 'login_scene'
        self.password = "password123"
        self.standard_sound_files = [
            "src/assets/sounds/single_keypress_01.wav",
            "src/assets/sounds/single_keypress_02.wav",
            "src/assets/sounds/single_keypress_03.wav",
            "src/assets/sounds/single_keypress_04.wav",
            "src/assets/sounds/single_keypress_05.wav",
            "src/assets/sounds/single_keypress_06.wav",
            "src/assets/sounds/single_keypress_07.wav",
            "src/assets/sounds/single_keypress_08.wav",
        ]
        self.enter_sound_files = [
            "src/assets/sounds/enter_keypress_01.wav",
            "src/assets/sounds/enter_keypress_02.wav",
            "src/assets/sounds/enter_keypress_03.wav",
        ]