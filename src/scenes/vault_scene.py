import pygame
from src.scenes.base_scene import BaseScene
from src.world.vault import Vault
from src.world.vault_renderer import VaultRenderer

class VaultScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.cell_size = 10
        self.vault_width = (app.screen.width // self.cell_size)
        self.vault_height = (app.screen.height // self.cell_size)
        self.vault = None
        self.renderer = None
        self.player_pos = None
        self.move_direction = None
        self.move_delay = 50  # Delay in milliseconds between each move when holding a key
        self.last_move_time = 0

    def enter(self):
        self.vault = Vault(self.vault_width, self.vault_height, self.cell_size)
        self.renderer = VaultRenderer(self.vault, self.cell_size)
        self.player_pos = self.vault.start_pos
        self.move_direction = None
        self.last_move_time = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move_direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                self.move_direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                self.move_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.move_direction = (1, 0)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                self.move_direction = None
        return False

    def update(self):
        if self.move_direction is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_move_time >= self.move_delay:
                x, y = self.player_pos
                dx, dy = self.move_direction
                new_pos = (x + dx, y + dy)
                new_x, new_y = new_pos

                if 0 <= new_x < self.vault.width and 0 <= new_y < self.vault.height:
                    if self.vault.layout[new_y][new_x] != self.vault.WALL:
                        self.player_pos = new_pos

                if self.player_pos == self.vault.exit_pos:
                    self.app.set_scene('success_scene')
                    return False

                self.last_move_time = current_time

    def render(self):
        self.app.screen.clear()
        self.renderer.render(self.app.screen.overlay, self.player_pos)
        self.app.screen.display(pygame.time.get_ticks())

