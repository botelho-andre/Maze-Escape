import pygame
import client_stub

# Definição das constantes para os movimentos
MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3


class Player(pygame.sprite.DirtySprite):
    def __init__(self, number: int, name: str, x: int, y: int, color: tuple[int, int, int], speed: float, maze: list, *groups):
        super().__init__(*groups)
        self.number = number
        self.name = name
        self.position = (x, y)
        self.width = 10
        self.height = 10
        self.color = color
        self.cell_width = 9
        self.cell_height = 9
        self.speed = speed
        self.maze = maze

    def update(self, stub: client_stub.StubClient) -> None:
        pos = stub.update("player", self.number)
        if self.position[0] != pos[0]:
            self.position = (pos[0], self.position[1])
        if self.position[1] != pos[1]:
            self.position = (self.position[0], pos[1])

    def draw_player(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color,
                         (self.position[0] * self.cell_width, self.position[1] * self.cell_height, self.cell_width,
                          self.cell_height))
