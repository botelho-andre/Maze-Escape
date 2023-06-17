import time
import pygame
import constants
from player_client import Player
import player_other
import client_stub


class GameUI(object):
    def __init__(self, stub: client_stub.StubClient) -> None:
        self.stub = stub
        self.players_dict = None
        self.players = None
        self.my_nr = None
        xy_max = self.stub.get_dim_game()  # obtém dimensões do jogo através do stub
        self.x_max, self.y_max = xy_max[0], xy_max[1]
        xy_cell_max = self.stub.get_cell_dim_game()  # obtém dimensões das células do jogo através do stub
        self.x_cell_max, self.y_cell_max = xy_cell_max[0], xy_cell_max[1]
        self.maze_lst = self.stub.get_maze_lst()  # obtém a lista do labirinto através do stub

        # Cores RGB
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gold = (255, 215, 0)
        self.red = (255, 0, 0)
        self.green = (0, 128, 0)
        self.player_color = [self.red, self.green]  # lista para a cor de cada jogador

        # Calcula as dimensões da superfície do labirinto
        self.surface_width = self.x_max * self.x_cell_max
        self.surface_height = self.y_max * self.y_cell_max
        # Cria a janela
        self.screen = pygame.display.set_mode((self.surface_width, self.surface_height))
        # Define o título da janela
        pygame.display.set_caption("Maze Escape")
        # Cria a superfície do labirinto
        self.maze_surface = pygame.Surface((self.surface_width, self.surface_height))
        # Desenha o labirinto na superfície
        self.draw_maze()
        # Redimensiona a superfície para o tamanho da janela
        self.maze_surface = pygame.transform.scale(self.maze_surface, (self.screen.get_width(), self.screen.get_height()))

    def draw_maze(self) -> None:
        for y in range(len(self.maze_lst)):
            for x in range(len(self.maze_lst[0])):
                if self.stub.get_wall_type(constants.GET_IS_WALL, x, y) is True:
                    pygame.draw.rect(self.maze_surface, self.black, (x * self.x_cell_max, y * self.y_cell_max,
                                                                     self.x_cell_max, self.y_cell_max))
                elif self.stub.get_wall_type(constants.GET_IS_MID_WALL, x, y) is True:
                    pygame.draw.rect(self.maze_surface, self.gold, (x * self.x_cell_max, y * self.y_cell_max,
                                                                    self.x_cell_max, self.y_cell_max))
                elif self.stub.get_wall_type(constants.GET_IS_P1_GOAL, x, y) is True:
                    pygame.draw.rect(self.maze_surface, self.red, (x * self.x_cell_max, y * self.y_cell_max,
                                                                   self.x_cell_max, self.y_cell_max))
                elif self.stub.get_wall_type(constants.GET_IS_P2_GOAL, x, y) is True:
                    pygame.draw.rect(self.maze_surface, self.green, (x * self.x_cell_max, y * self.y_cell_max,
                                                                     self.x_cell_max, self.y_cell_max))
                else:
                    pygame.draw.rect(self.maze_surface, self.white, (x * self.x_cell_max, y * self.y_cell_max,
                                                                     self.x_cell_max, self.y_cell_max))

    def set_players(self) -> None:
        self.players_dict = self.stub.get_players()
        nr_players = self.stub.get_nr_players()
        self.players = pygame.sprite.LayeredDirty()
        print("Client: Current number of players:", nr_players)
        print("Client: Players information:", self.players_dict)
        for nr in range(nr_players):
            if self.players_dict[str(nr)]:
                p_x, p_y = self.players_dict[str(nr)][1][0], self.players_dict[str(nr)][1][1]
                if self.my_nr == nr:
                    player = Player(nr, self.players_dict[str(nr)][0], p_x, p_y, self.player_color[nr], 0.2, self.maze_lst)
                else:
                    player = player_other.Player(nr, self.players_dict[str(nr)][0], p_x, p_y, self.player_color[nr], 0.2, self.maze_lst)
                self.players.add(player)

    def run(self) -> bool:
        print("Client: Welcome to Maze Escape!")
        name = input("Client: Please enter your name: ")
        print("Client: Hello " + name + "! You're in, get ready!")
        self.my_nr = self.stub.add_player(name)
        print("Client: Waiting for an opponent...")
        self.stub.start_game()
        self.set_players()
        play_music()

        end = False
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True

            self.screen.blit(self.maze_surface, (0, 0))
            for player in self.players:
                player.update(self.stub)
                player.draw_player(self.screen)
                if self.stub.get_is_player_at_goal(player.number, player.position[0], player.position[1]) is True:
                    print("Client: Game ended")
                    pygame.mixer.music.stop()
                    play_win_sound()
                    show_winner_screen(self.screen, player.name)
                    time.sleep(12)
                    end = True

            pygame.display.update()
        return True


def show_winner_screen(screen, winner_name):
    screen.fill((0, 0, 0))  # cor preta
    font = pygame.font.Font(None, 36)  # cria uma fonte para o texto

    text = font.render("Winner: " + winner_name, True, (255, 255, 255))  # cor branca
    text_rect = text.get_rect(center=screen.get_rect().center)
    screen.blit(text, text_rect)

    second_text = font.render("Thanks for playing Maze Escape!", True, (255, 255, 255))
    second_text_rect = second_text.get_rect(center=(screen.get_width() // 2, text_rect.bottom + 20))
    screen.blit(second_text, second_text_rect)

    pygame.display.flip()  # atualiza a tela


def play_music():
    pygame.mixer.music.load("the-art-of-synths.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


def play_win_sound():
    pygame.mixer.music.load("winner-bell.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(0)
