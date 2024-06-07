import pygame
from pygame import mixer
from src.scenes.scene_factory import SceneFactory
import random
import time  # Import time for calculating elapsed time

class Application:
    def __init__(self, screen, text_renderer, input_handler, config):
        self.screen = screen
        self.text_renderer = text_renderer
        self.input_handler = input_handler
        self.config = config
        self.scenes = SceneFactory.create_scenes(self, config)
        self.active_scene = None
        self.is_rendering = True
        self.state_transition = False
        self.standard_sounds, self.enter_sounds = self._load_sounds()
        self.start_time = time.time()  # Track the start time

    def run(self):
        self._initialize()
        clock = pygame.time.Clock()
        done = False

        while not done:
            current_time = time.time() - self.start_time  # Calculate elapsed time
            for event in pygame.event.get():
                done |= self.active_scene.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    self._play_key_sound(event.key)

            self.active_scene.update()
            self.screen.clear()
            self.active_scene.render()
            self.screen.display(current_time)  # Pass current time to display method
            clock.tick(60)

        pygame.quit()

    def _initialize(self):
        self.screen.initialize()
        self.set_scene(self.config.initial_scene)

    def set_scene(self, scene_name):
        self.active_scene = self.scenes[scene_name]
        self.text_renderer.reset_previous_lines()
        self.active_scene.enter()

    def _load_sounds(self):
        mixer.init()
        mixer.set_num_channels(16)

        standard_sounds = [mixer.Sound(file) for file in self.config.standard_sound_files]
        enter_sounds = [mixer.Sound(file) for file in self.config.enter_sound_files]

        return standard_sounds, enter_sounds

    def _play_key_sound(self, key):
        sound_list = self.enter_sounds if key == pygame.K_RETURN else self.standard_sounds
        sound = random.choice(sound_list)
        sound.play()
