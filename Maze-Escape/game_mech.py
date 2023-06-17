import csv

# Definição das constantes para os movimentos
MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3


class GameMech:
    def __init__(self) -> None:
        # Guarda o nome do ficheiro csv com o mapa do labirinto
        self.maze_file = str("maze.csv")

        # Lê o ficheiro csv e guarda informações do mapa do labirinto numa lista
        with open(self.maze_file, 'r') as file:
            self.maze = []
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                self.maze.append(row)

        # Calcula as dimensões máximas (x,y) da matriz do labirinto
        self.x_max = len(self.maze[0])
        self.y_max = len(self.maze)
        # Define o tamanho de cada célula
        self.x_cell_max = 9
        self.y_cell_max = 9
        # Lista de jogadores
        self.players = dict()
        # Lista de obstáculos
        self.obstacles = dict()
        # Número de jogadores e obstáculos no jogo
        self.nr_players = 0
        self.nr_obstacles = 0

        # Posições (x, y) iniciais de cada jogador
        self.pl_start_pos = {0: (1, 78), 1: (78, 1)}
        # Posições (x, y) da meta dos dois jogadores
        self.goals_pos = {0: (39, 40), 1: (40, 39)}

        # Inicia o mundo vazio
        self.world = dict()
        for i in range(self.x_max):
            for j in range(self.y_max):
                self.world[(i, j)] = []

        # Adiciona obstáculos ao mundo
        self.create_world()

    # Verifica se a posição atual é uma parede normal
    def is_wall(self, x: int, y: int) -> bool:
        return self.maze[y][x] == "#"

    # Verifica se a posição atual é a parede central
    def is_mid_wall(self, x: int, y: int) -> bool:
        return self.maze[y][x] == "$"

    # Verifica se a posição atual é a meta do jogador 1
    def is_p1_goal(self, x: int, y: int) -> bool:
        return self.maze[y][x] == "1"

    # Verifica se a posição atual é a meta do jogador 2
    def is_p2_goal(self, x: int, y: int) -> bool:
        return self.maze[y][x] == "2"

    # Verifica se existe um obstáculo na posição
    def obstacle_exists(self, x_pos: int, y_pos: int) -> bool:
        for obj in self.world[(x_pos, y_pos)]:
            if obj[0] == "obstacle":
                return True
        return False

    # Adiciona obstáculo ao mundo
    def add_obstacle(self, type: str, x_pos: int, y_pos: int) -> bool:
        if self.obstacle_exists(x_pos, y_pos):
            return False
        nr_obstacles = self.nr_obstacles
        self.obstacles[nr_obstacles] = [type, (x_pos, y_pos)]
        self.world[(x_pos, y_pos)].append(["obstacle", type, nr_obstacles, (x_pos, y_pos)])
        self.nr_obstacles += 1
        return True

    # Verifica se existe um obstáculo de um determinado tipo numa posição
    def is_obstacle(self, type, x: int, y: int) -> bool:
        for i in self.world[(x, y)]:
            if i[0] == "obstacle" and i[1] == type:
                return True
        return False

    # Adiciona um novo jogador ao mundo
    def add_player(self, name: str) -> int:
        nr_player = self.nr_players
        self.players[nr_player] = [name, self.pl_start_pos[nr_player]]
        self.world[self.pl_start_pos[nr_player]].append(["player", name, nr_player, self.pl_start_pos[nr_player]])
        self.nr_players += 1
        return nr_player

    # Cria o mundo com base no labirinto fornecido
    def create_world(self) -> None:
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                if self.is_wall(x, y) or self.is_mid_wall(x, y) is True:
                    self.add_obstacle("wall", x, y)

    # Executar movimento do jogador
    def execute(self, move: int, type: str, nr_player: int) -> tuple:
        if type == "player":
            name = self.players[nr_player][0]
            print("Player:", name)
            pos_x, pos_y = self.players[nr_player][1][0], self.players[nr_player][1][1]

            if move == MOVE_LEFT:
                new_pos_x = pos_x - 1
                new_pos_y = pos_y
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_x = pos_x
            elif move == MOVE_RIGHT:
                new_pos_x = pos_x + 1
                new_pos_y = pos_y
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_x = pos_x
            elif move == MOVE_UP:
                new_pos_y = pos_y - 1
                new_pos_x = pos_x
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_y = pos_y
            elif move == MOVE_DOWN:
                new_pos_y = pos_y + 1
                new_pos_x = pos_x
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_y = pos_y
            else:
                new_pos_x = pos_x
                new_pos_y = pos_y

            self.players[nr_player] = [name, (new_pos_x, new_pos_y)]
            world_pos = self.world[(pos_x, pos_y)]
            world_pos.remove(["player", name, nr_player, (pos_x, pos_y)])
            self.world[(pos_x, pos_y)] = world_pos
            self.world[(new_pos_x, new_pos_y)].append(["player", name, nr_player, (new_pos_x, new_pos_y)])
            return new_pos_x, new_pos_y

    def print_world(self) -> None:
        for i in range(self.x_max):
            for j in range(self.y_max):
                print("(", i, ",", j, ") =", self.world[(i, j)])

    def print_players(self) -> None:
        for p in self.players:
            print("Nr. ", p)
            print("Value:", self.players[p])

    def is_player_at_goal(self, player_number: int, player_position: tuple[int, int]) -> bool:
        if player_number in self.goals_pos and player_position == self.goals_pos[player_number]:
            return True
        else:
            return False

    def print_pos(self, x: int, y: int):
        print("(x= ", x, ", y=", y, ") =", self.world[(x, y)])

    def get_players(self) -> dict:
        return self.players

    def get_obstacles(self) -> dict:
        return self.obstacles

    def get_nr_obstacles(self) -> int:
        return self.nr_obstacles

    def get_nr_players(self):
        return self.nr_players

    def get_x_max(self) -> int:
        return self.x_max

    def get_y_max(self) -> int:
        return self.y_max


# Testing Game Mechanics
if __name__ == '__main__':
    gm = GameMech()
    gm.create_world()
    gm.get_obstacles()
    nr_player = gm.add_player("jogador1")
    gm.print_world()
    gm.print_players()
    gm.print_pos(1, 78)
    print(gm.execute(MOVE_RIGHT, "player", 0))
