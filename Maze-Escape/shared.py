import socket
import constants
import threading
from typing import Set


class Shared:
    """
    — classe tem o objetivo de dar permissão através de locks
    — acesso de dados partilhados por mais do que uma thread.
    — faz a ponte entre o pedido de execução de uma ação e a permissão para essa ação através do lock.
    — guarda o número de clientes ligados, desbloqueando o arranque do jogo apenas quando existe 2 clientes ligados.

    Semáforo:
    — Quando está zero, o semáforo bloqueia todos os que vão para a sua fila.
    — Quando um recebe instrução -1, permite passar o primeiro thread que está na fila e fica a zero novamente.
    — Se o semáforo ficar a 2, passam os primeiros dois threads e o semáforo fica a zero.
    — Se o semáforo for x, e se passam z threads, o semáforo fica x-z, ou zero se z >= x.
    """
    def __init__(self):
        # Um conjunto não permite ter clientes iguais. No conjunto iremos guardar os ‘sockets’ dos clientes.
        self._clients: Set[socket.socket] = set()
        self._clients_lock = threading.Lock()
        self._clients_control = threading.Semaphore(0)  # Semáforo impedindo os clientes de arrancar

    def add_client(self, client: socket.socket) -> None:
        """
        Adiciona um cliente à lista de clientes de forma protegida
        :param client:
        :return:
        """
        self._clients_lock.acquire()
        self._clients.add(client)
        self._clients_lock.release()

    def remove_client(self, client_socket: socket.socket) -> None:
        """
        Remove cliente. Se o número de clientes é menor que o número máximo, permite
        a entrada de mais um, abrindo o semáforo para passar apenas 1 (semáforo fica 1)
        :param self:
        :param client_socket:
        :return:
        """
        self._clients_lock.acquire()
        self._clients.remove(client_socket)
        if len(self._clients) < constants.NR_CLIENTS:
            # indica que existe um cliente que pode entrar
            self._clients_control.release()
        self._clients_lock.release()

    def control_nr_clients(self):
        print("Server: New client received! Nr. of clients:", len(self._clients))
        if len(self._clients) >= constants.NR_CLIENTS:
            print("Server: Number of clients:", len(self._clients))
            print("Server: Game started!")
            for i in range(len(self._clients)):
                # permite o número exato de clientes começando o jogo
                self._clients_control.release()
