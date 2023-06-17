from game_mech import GameMech
from server_skeleton import SkeletonServer


def main():
    """
    Inicia o Game Mechanics (gm) e quem vai correr o programa no servidor é o
    skeleton que está sempre à escuta da informação que vem do lado do cliente.
    :return:
    """
    print("\n---------- Maze Escape Server ----------")
    print("\nServer: Starting the server...")
    print("Server: Starting game mechanics...")
    gm = GameMech()
    skeleton = SkeletonServer(gm)
    skeleton.run()


main()
