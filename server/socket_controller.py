import socket
import sys
from threading import Thread

import select


class SocketController:
    def __init__(self, max_players: int, port: int):
        self.__max_players = max_players
        self.__port = port
        self.__finished = False
        self.__connected_clients = {}

    def read_keyboard(self):
        while not self.__finished:
            quit_command = input()
            if quit_command == 'q':
                self.__finished = True

    def start_listen(self):
        server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_tcp_socket.bind(('', self.__port))
        server_tcp_socket.listen(5)

        server_upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_upd_socket.bind(('', self.__port))

        print("Type q to quit the session")

        keyboard_input = Thread(target=self.read_keyboard)
        keyboard_input.start()

        while not self.__finished:
            read_sockets, write_sockets, error_sockets = select.select(
                [server_tcp_socket, server_upd_socket],
                [],
                [],
                0
            )
            for sock in read_sockets:
                if sock == server_tcp_socket:
                    self.__handle_tcp(server_tcp_socket)
                elif sock == server_upd_socket:
                    self.__handle_udp(server_upd_socket)

    def __handle_tcp(self, server_tcp_socket):
        server_tcp_socket.accept()

    def __handle_udp(self, server_udp_socket):
        pass
