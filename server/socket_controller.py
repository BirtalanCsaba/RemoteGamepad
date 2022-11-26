import socket
import sys

import select


class SocketController:
    def __init__(self, max_players: int, port: int):
        self.__max_players = max_players
        self.__port = port

    def start_listen(self):
        server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_tcp_socket.bind(('', self.__port))
        server_tcp_socket.listen(5)

        server_upd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_upd_socket.bind(('', self.__port))

        finished = False
        while not finished:
            read_sockets, write_sockets, error_sockets = select.select(
                [sys.stdin, server_tcp_socket, server_upd_socket],
                [],
                []
            )

            for sock in read_sockets:
                if sock == server_tcp_socket:
                    pass
                elif sock == server_upd_socket:
                    pass
                elif sock == sys.stdin:
                    pass
