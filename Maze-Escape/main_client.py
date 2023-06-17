import pygame
from client_stub import StubClient
from client_game import GameUI


def main():
    """
    Inicia o stub e a parte de topo do cliente que vai correr.
    :return:
    """
    print("\n---------- Maze Escape Client ----------")
    print("\nClient: Starting client connection...")
    pygame.init()
    stub = StubClient()
    ui = GameUI(stub)
    print("Client: Client started...")
    ui.run()


main()
