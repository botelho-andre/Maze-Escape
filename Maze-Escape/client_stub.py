import json
import socket
import constants


# Stub do lado do cliente: comunicação com o servidor

class StubClient:
    def __init__(self):  # inicio do socket do lado do cliente
        self.s: socket = socket.socket()
        self.s.connect((constants.SERVER_ADDRESS, constants.PORT))

    def get_dim_game(self) -> tuple:
        """
        Protocolo:
        — enviar mensagem com nome associado ao pedido x_max e y_max.
        — servidor retorna dois inteiros com essa informação.
        :return:
        """
        self.s.send(constants.X_MAX.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        x_max = int.from_bytes(data, byteorder='big', signed=True)
        self.s.send(constants.Y_MAX.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        y_max = int.from_bytes(data, byteorder='big', signed=True)
        return x_max, y_max

    def get_cell_dim_game(self) -> tuple:
        """
        Protocolo:
        — enviar mensagem ao servidor com nome associado ao pedido x_cell_max e y_cell_max.
        — servidor retorna dois inteiros com essa informação.
        :return:
        """
        self.s.send(constants.X_CELL_MAX.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        x_cell_max = int.from_bytes(data, byteorder='big', signed=True)
        self.s.send(constants.Y_CELL_MAX.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        y_cell_max = int.from_bytes(data, byteorder='big', signed=True)
        return x_cell_max, y_cell_max

    def get_maze_lst(self) -> list:
        """
        Protocolo:
        — enviar mensagem ao servidor com nome associado ao pedido get_maze.
        — servidor retorna a lista com essa informação.
        :return:
        """
        self.s.send(constants.GET_MAZE.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        maze_lst = json.loads(rec)
        return maze_lst

    def get_wall_type(self, wall_type: str, x: int, y: int) -> bool:
        """
        Protocolo:
        — enviar mensagem ao servidor para obter o tipo de parede na posição especificada.
        :param wall_type: o tipo de parede
        :param x: a posição x
        :param y: a posição y
        :return: true/false se é um determinado tipo de parede
        """
        self.s.send(wall_type.encode(constants.STR_COD))
        self.s.send(x.to_bytes(constants.N_BYTES, byteorder='big', signed=True))
        self.s.send(y.to_bytes(constants.N_BYTES, byteorder='big', signed=True))
        data: bytes = self.s.recv(constants.N_BYTES)
        result = bool.from_bytes(data, byteorder='big', signed=True)
        return result

    def add_player(self, name: str) -> int:
        """
        Protocolo:
        — enviar mensagem ao servidor para adicionar um jogador com o nome fornecido.
        :param name: o nome do jogador a ser adicionado
        :return: o número atribuído ao jogador adicionado
        """
        self.s.send(constants.ADD_PLAYER.encode(constants.STR_COD))
        self.s.send(name.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        number = int.from_bytes(data, byteorder='big', signed=True)
        return number

    def update(self, type:str, number: int) -> tuple:
        """
        — enviar mensagem de atualização ao servidor com o número específico.
        — servidor retorna um tuplo com os dados atualizados.
        :return:
        """
        self.s.send(constants.UPDATE.encode(constants.STR_COD))
        self.s.send(number.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        data: bytes = self.s.recv(constants.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        _tuple = json.loads(rec)
        return _tuple

    def get_players(self) -> dict:
        """
        Protocolo:
        — envia mensagem ao servidor associado ao pedido get_players.
        — recebe dimensão do objeto dicionário.
        — recebe objeto dicionário com todos os jogadores.
        :return:
        """
        self.s.send(constants.GET_PLAYERS.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        players = json.loads(rec)
        return players

    def get_nr_players(self) -> None:
        """
        Protocolo:
        — envia mensagem ao servidor pedindo o número de jogadores.
        — servidor retorna número de jogadores.
        :return:
        """
        self.s.send(constants.NR_PLAYERS.encode(constants.STR_COD))
        data: bytes = self.s.recv(constants.N_BYTES)
        nr = int.from_bytes(data, byteorder='big', signed=True)
        return nr

    def start_game(self) -> None:
        """
        — Pede ao servidor para iniciar o jogo.
        — Servidor retornará sim quando o número de jogadores for 2.
        :return:
        """
        self.s.send(constants.START_GAME.encode(constants.STR_COD))
        rec: bytes = self.s.recv(constants.N_BYTES)
        res = rec.decode(constants.STR_COD)
        print("Client: Starting the Game:", res)

    def execute(self, mov: int, type:str, player: int) -> tuple:
        """
        Protocolo:
        — envia mensagem ao servidor associado ao pedido "PLAYER_MOV".
        — envia o movimento e nr do jogador.
        — recebe a nova posição do jogador (tuplo).
        """
        self.s.send(constants.PLAYER_MOV.encode(constants.STR_COD))
        self.s.send(mov.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        self.s.send(player.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        data: bytes = self.s.recv(constants.N_BYTES)
        dim = int.from_bytes(data, byteorder='big', signed=True)
        rec: bytes = self.s.recv(dim)
        _tuple = json.loads(rec)
        return _tuple

    def get_is_player_at_goal(self, player_number: int, x_pos: int, y_pos: int) -> bool:
        """
        Protocolo:
        — envia mensagem ao servidor associado ao pedido "GET_IS_PLAYER_AT_GOAL".
        :param player_number: número do jogador
        :param x_pos: posição x do jogador
        :param y_pos: posição y do jogador
        :return: true se o jogador estiver na posição do objetivo, falso caso contrário
        """
        self.s.send(constants.GET_IS_PLAYER_AT_GOAL.encode(constants.STR_COD))
        self.s.send(player_number.to_bytes(constants.N_BYTES, byteorder='big', signed=True))
        self.s.send(x_pos.to_bytes(constants.N_BYTES, byteorder='big', signed=True))
        self.s.send(y_pos.to_bytes(constants.N_BYTES, byteorder='big', signed=True))
        data: bytes = self.s.recv(constants.N_BYTES)
        result = bool.from_bytes(data, byteorder='big', signed=True)
        return result
