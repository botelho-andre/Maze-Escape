from threading import Thread
from game_mech import GameMech
import constants
import json
import logging
import shared


class ClientSession(Thread):
    """Maintains a session with the client"""

    def __init__(self, socket_client: int, shr: shared.Shared, game_mech: GameMech):
        """
        Constructs a thread to hold a session with the client
        :param shared_state: The server's state shared by threads
        :param client_socket: The client's socket
        """
        Thread.__init__(self)
        self._shared = shr
        self.socket_client = socket_client
        self.gm = game_mech

    def process_x_max(self, s_c):
        x = self.gm.x_max
        s_c.send(x.to_bytes(constants.N_BYTES, byteorder="big", signed=True))

    def process_y_max(self, s_c):
        y = self.gm.y_max
        s_c.send(y.to_bytes(constants.N_BYTES, byteorder="big", signed=True))

    def process_x_cell_max(self, s_c):
        x_cell = self.gm.x_cell_max
        s_c.send(x_cell.to_bytes(constants.N_BYTES, byteorder="big", signed=True))

    def process_y_cell_max(self, s_c):
        y_cell = self.gm.y_cell_max
        s_c.send(y_cell.to_bytes(constants.N_BYTES, byteorder="big", signed=True))

    def process_get_maze_lst(self, s_c):
        maze_lst = self.gm.maze
        msg = json.dumps(maze_lst)
        dim = len(msg)
        s_c.send(dim.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constants.STR_COD))

    def process_get_wall_type(self, s_c, wall_type_func):
        data_rcv: bytes = s_c.recv(constants.N_BYTES)
        x = int.from_bytes(data_rcv, byteorder='big', signed=True)
        data_rcv: bytes = s_c.recv(constants.N_BYTES)
        y = int.from_bytes(data_rcv, byteorder='big', signed=True)
        result = wall_type_func(x, y)
        s_c.send(result.to_bytes(constants.N_BYTES, byteorder='big', signed=True))

    def process_get_is_wall(self, s_c):
        self.process_get_wall_type(s_c, self.gm.is_wall)

    def process_get_is_mid_wall(self, s_c):
        self.process_get_wall_type(s_c, self.gm.is_mid_wall)

    def process_get_is_p1_goal(self, s_c):
        self.process_get_wall_type(s_c, self.gm.is_p1_goal)

    def process_get_is_p2_goal(self, s_c):
        self.process_get_wall_type(s_c, self.gm.is_p2_goal)

    def process_add_player(self, s_c):
        data_rcv: bytes = s_c.recv(constants.MSG_SIZE)
        name = data_rcv.decode(constants.STR_COD)
        number = self.gm.add_player(name)
        self._shared.add_client(s_c)
        self._shared.control_nr_clients()
        s_c.send(number.to_bytes(constants.N_BYTES, byteorder="big", signed=True))

    def process_get_players(self, s_c):
        pl = self.gm.players
        msg = json.dumps(pl)
        dim = len(msg)
        s_c.send(dim.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constants.STR_COD))

    def process_get_nr_players(self, s_c):
        nr_pl = self.gm.nr_players
        s_c.send(nr_pl.to_bytes(constants.N_BYTES, byteorder="big", signed=True))

    def process_player_mov(self, s_c):
        data: bytes = s_c.recv(constants.N_BYTES)
        mov = int.from_bytes(data, byteorder='big', signed=True)
        data: bytes = s_c.recv(constants.N_BYTES)
        nr_player = int.from_bytes(data, byteorder='big', signed=True)
        pos = self.gm.execute(mov, "player", nr_player)
        msg = json.dumps(pos)
        dim = len(msg)
        s_c.send(dim.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constants.STR_COD))

    def process_get_is_player_at_goal(self, s_c):
        data_rcv: bytes = s_c.recv(constants.N_BYTES)
        player_number = int.from_bytes(data_rcv, byteorder='big', signed=True)
        data_rcv: bytes = s_c.recv(constants.N_BYTES)
        x = int.from_bytes(data_rcv, byteorder='big', signed=True)
        data_rcv: bytes = s_c.recv(constants.N_BYTES)
        y = int.from_bytes(data_rcv, byteorder='big', signed=True)
        result = self.gm.is_player_at_goal(player_number, (x, y))
        s_c.send(result.to_bytes(constants.N_BYTES, byteorder='big', signed=True))

    def process_start_game(self, s_c):
        logging.debug("O client pretende inciar o jogo")
        self._shared._clients_control.acquire()
        logging.debug("O client vai iniciar o jogo")
        # Returning 'yes'
        value = constants.TRUE
        s_c.send(value.encode(constants.STR_COD))

    def process_update(self, s_c):
        logging.debug("O client pede um update")
        pl: bytes = s_c.recv(constants.N_BYTES)
        number = int.from_bytes(pl, byteorder='big', signed=True)
        pos = self.gm.players[number][1]
        msg = json.dumps(pos)
        size = len(msg)  # obter o tamanho dos dados
        s_c.send(size.to_bytes(constants.N_BYTES, byteorder="big", signed=True))
        s_c.send(msg.encode(constants.STR_COD))

    def dispatch_request(self, socket_client) -> bool:
        lr = False
        data_rcv: bytes = socket_client.recv(constants.MSG_SIZE)
        data_str = data_rcv.decode(constants.STR_COD)
        logging.debug("o cliente enviou: \"" + data_str + "\"")
        if data_str == constants.X_MAX:
            self.process_x_max(socket_client)
        elif data_str == constants.Y_MAX:
            self.process_y_max(socket_client)
        elif data_str == constants.X_CELL_MAX:
            self.process_x_cell_max(socket_client)
        elif data_str == constants.Y_CELL_MAX:
            self.process_y_cell_max(socket_client)
        elif data_str == constants.ADD_PLAYER:
            self.process_add_player(socket_client)
        elif data_str == constants.GET_PLAYERS:
            self.process_get_players(socket_client)
        elif data_str == constants.NR_PLAYERS:
            self.process_get_nr_players(socket_client)
        elif data_str == constants.PLAYER_MOV:
            self.process_player_mov(socket_client)
        elif data_str == constants.GET_MAZE:
            self.process_get_maze_lst(socket_client)
        elif data_str == constants.GET_IS_WALL:
            self.process_get_is_wall(socket_client)
        elif data_str == constants.GET_IS_MID_WALL:
            self.process_get_is_mid_wall(socket_client)
        elif data_str == constants.GET_IS_P1_GOAL:
            self.process_get_is_p1_goal(socket_client)
        elif data_str == constants.GET_IS_P2_GOAL:
            self.process_get_is_p2_goal(socket_client)
        elif data_str == constants.GET_IS_PLAYER_AT_GOAL:
            self.process_get_is_player_at_goal(socket_client)
        elif data_str == constants.START_GAME:  # --------------------------- Começar o jogo
            self.process_start_game(socket_client)
        elif data_str == constants.UPDATE:
            self.process_update(socket_client)
        elif data_str == constants.END:
            lr = True
        return lr

    def run(self):
        """Maintains a session with the client, following the established protocol"""
        last_request = False
        while not last_request:
            last_request = self.dispatch_request(self.socket_client)
        logging.debug("Client " + str(self.socket_client.peer_addr) + " disconnected")
