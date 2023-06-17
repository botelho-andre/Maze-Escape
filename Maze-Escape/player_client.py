import pygame
import time
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
        # Verifica quais teclas estão pressionadas
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            print("Client: Player pressed left key")
            pos = stub.execute(MOVE_LEFT, "player", self.number)
            print("Client: Current position: ", pos, "\n")
            if self.position[0] != pos[0]:
                self.position = (pos[0], self.position[1])
        if key[pygame.K_RIGHT]:
            print("Client: Player pressed right key")
            pos = stub.execute(MOVE_RIGHT, "player", self.number)
            print("Client: Current position: ", pos, "\n")
            if self.position[0] != pos[0]:
                self.position = (pos[0], self.position[1])
        if key[pygame.K_UP]:
            print("Client: Player pressed up key")
            pos = stub.execute(MOVE_UP, "player", self.number)
            print("Client: Current position: ", pos, "\n")
            if self.position[1] != pos[1]:
                self.position = (self.position[0], pos[1])
        if key[pygame.K_DOWN]:
            print("Client: Player pressed down key")
            pos = stub.execute(MOVE_DOWN, "player", self.number)
            print("Client: Current position: ", pos, "\n")
            if self.position[1] != pos[1]:
                self.position = (self.position[0], pos[1])
        time.sleep(self.speed)

    def draw_player(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color,
                         (self.position[0] * self.cell_width, self.position[1] * self.cell_height, self.cell_width,
                          self.cell_height))
