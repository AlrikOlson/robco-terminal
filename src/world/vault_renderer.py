import pygame

class VaultRenderer:
    COLORS = {
        0: (100, 100, 100),  # Wall
        1: (200, 200, 200),  # Floor
        2: (0, 255, 0),  # Start
        3: (255, 0, 0),  # Exit
        4: (139, 69, 19),  # Door
        5: (255, 165, 0),  # Atrium,
        6: (200, 200, 200),  # Hallway
    }

    def __init__(self, vault, cell_size=20):
        self.vault = vault
        self.cell_size = cell_size

    def render(self, screen, player_pos):
        for y in range(self.vault.height):
            for x in range(self.vault.width):
                cell_type = self.vault.layout[y][x]
                if cell_type == self.vault.EXIT:
                    self._render_exit(screen, x, y)
                else:
                    color = self.COLORS[cell_type]
                    rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, color, rect)
        self._render_player(screen, player_pos)

    def _render_exit(self, screen, x, y):
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.COLORS[3], rect)
        checker_size = self.cell_size // 4
        for i in range(4):
            for j in range(4):
                if (i + j) % 2 == 0:
                    checker_rect = pygame.Rect(
                        x * self.cell_size + i * checker_size,
                        y * self.cell_size + j * checker_size,
                        checker_size,
                        checker_size
                    )
                    pygame.draw.rect(screen, (255, 255, 255), checker_rect)

    def _render_player(self, screen, player_pos):
        x, y = player_pos
        player_color = (0, 0, 255)  # Blue
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, player_color, rect)
