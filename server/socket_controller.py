import json
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock

import select
from vgamepad import VX360Gamepad, XUSB_BUTTON

from common.models.axis_input_value import AxisInputValue
from common.models.axis_types import AxisTypes
from common.models.button_input import ButtonInput
from common.models.button_types import ButtonTypes
from common.models.connection_details import ConnectionDetails
from common.models.dpad_input import DpadInput
from common.models.dpad_types import DpadTypes
from server.remote_client import RemoteClient


class SocketController:
    def __init__(self, max_players: int, port: int):
        self.__max_players = max_players
        self.__port = port
        self.__finished = False
        self.__number_of_connected_client = 0
        self.__socket_inputs = {}
        self.__thread_pool = ThreadPoolExecutor(max_workers=10)
        self.__console_mutex = Lock()

    def __read_keyboard(self):
        while not self.__finished:
            quit_command = input()
            if quit_command == 'q':
                self.__finished = True

    def __print(self, message: str):
        self.__console_mutex.acquire()
        print(message)
        self.__console_mutex.release()

    def start_listen(self):
        server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_tcp_socket.bind(('', self.__port))
        server_tcp_socket.listen(5)
        server_tcp_socket.setblocking(False)

        server_upd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_upd_socket.bind(('', self.__port))
        server_upd_socket.setblocking(False)

        self.__socket_inputs[server_tcp_socket] = RemoteClient(None, None)
        self.__socket_inputs[server_upd_socket] = RemoteClient(None, None)

        self.__print("Type q to quit the session")

        keyboard_input = Thread(target=self.__read_keyboard)
        keyboard_input.start()

        while not self.__finished:
            read_sockets, write_sockets, error_sockets = select.select(
                self.__socket_inputs.keys(),
                [],
                [],
                0
            )
            for sock in read_sockets:
                if sock == server_tcp_socket:
                    self.__thread_pool.submit(self.__handle_tcp, sock)
                elif sock == server_upd_socket:
                    self.__handle_udp(sock)
                elif sock in self.__socket_inputs:
                    self.__thread_pool.submit(self.__handle_client, sock)

        self.__print("Shutting down ...")
        self.__thread_pool.shutdown(wait=False)
        self.__cleanup_resources()
        keyboard_input.join()

    def __cleanup_resources(self):
        for input_socket in self.__socket_inputs.keys():
            if self.__socket_inputs[input_socket].Name is None:
                self.__close_connection_with_socket(
                    input_socket,
                    remove_socket=False
                )
            else:
                self.__shutdown_connection_with_socket(
                    input_socket,
                    f"Closing connection with: {self.__socket_inputs[input_socket].Name}",
                    remove_socket=False
                )

    def __handle_client(self, client_sock):
        data = client_sock.recv(1024, )
        remote_client = self.__socket_inputs[client_sock]
        if not data:
            self.__shutdown_connection_with_socket(
                client_sock,
                f"Player with ip address: {remote_client.Address} and name: <<{remote_client.Name}>> connection lost."
            )
            return
        message = data.decode('utf-8')
        connection_details = ConnectionDetails.from_json(message)
        if not connection_details.validate():
            self.__shutdown_connection_with_socket(
                client_sock,
                f"Player with ip address: {remote_client.Address} failed to connect. Name too long."
            )
        remote_client.Name = connection_details.Name
        remote_client.IsConnected = True
        remote_client.Gamepad = VX360Gamepad()

        self.__print(f"Player with username: <<{remote_client.Name}>> successfully connected.")

    def __handle_tcp(self, server_tcp_socket):
        client_sock, client_addr = server_tcp_socket.accept()
        client_sock.setblocking(False)
        if client_addr in self.__socket_inputs:
            return
        self.__print(f"Player with address: {client_addr} is trying to connect.")
        self.__socket_inputs[client_sock] = RemoteClient(client_addr, None)

        time.sleep(5)

        if not self.__socket_inputs[client_sock].IsConnected:
            self.__shutdown_connection_with_socket(client_sock, f"Player with address {client_addr} timeout.")

    def __handle_udp(self, server_udp_socket):
        try:
            data, addr = server_udp_socket.recvfrom(1024)
        except socket.error:
            print("Cannot read controller input")
            return
        self.__thread_pool.submit(self.__do_controller_command, data, addr)

    def __do_controller_command(self, data, address):
        for remote_client in self.__socket_inputs.values():
            if remote_client.address == address:
                try:
                    message = json.loads(data.decode('utf-8'))
                    # print(message)
                except Exception:
                    continue

                if message["input_type"] == "button":
                    button_command = ButtonInput.from_json(message)
                    self.__handle_button_command(button_command, remote_client.Gamepad)
                    # print("button")
                elif message["input_type"] == "axis":
                    axis_command = AxisInputValue.from_json(message)
                    self.__handle_axis_command(axis_command, remote_client.Gamepad)
                    # print("axis")
                elif message["input_type"] == "dpad":
                    dpad_command = DpadInput.from_json(message)
                    self.__handle_dpad_command(dpad_command, remote_client.Gamepad)

    def __handle_button_command(self, command: ButtonInput, gamepad: VX360Gamepad):
        if command.Name == ButtonTypes.A.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif command.Name == ButtonTypes.B.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
        elif command.Name == ButtonTypes.X.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
        elif command.Name == ButtonTypes.Y.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
        elif command.Name == ButtonTypes.LEFT_BUTTON.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        elif command.Name == ButtonTypes.RIGHT_BUTTON.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        elif command.Name == ButtonTypes.MENU.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        elif command.Name == ButtonTypes.START.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_START)
        elif command.Name == ButtonTypes.L3.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        elif command.Name == ButtonTypes.R3.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

        elif command.Name == ButtonTypes.RELEASE_A.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif command.Name == ButtonTypes.RELEASE_B.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
        elif command.Name == ButtonTypes.RELEASE_X.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
        elif command.Name == ButtonTypes.RELEASE_Y.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
        elif command.Name == ButtonTypes.RELEASE_LEFT_BUTTON.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        elif command.Name == ButtonTypes.RELEASE_RIGHT_BUTTON.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        elif command.Name == ButtonTypes.RELEASE_MENU.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        elif command.Name == ButtonTypes.RELEASE_START.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_START)
        elif command.Name == ButtonTypes.RELEASE_L3.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        elif command.Name == ButtonTypes.RELEASE_R3.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

        gamepad.update()

    def __handle_axis_command(self, command: AxisInputValue, gamepad: VX360Gamepad):
        if command.AxisInput.Name == AxisTypes.LSB_LEFT_RIGHT.Name:
            gamepad.left_joystick_float(command.XValue, -command.YValue)
        elif command.AxisInput.Name == AxisTypes.LSB_TOP_DOWN.Name:
            gamepad.left_joystick_float(command.XValue, -command.YValue)
        elif command.AxisInput.Name == AxisTypes.RSB_LEFT_RIGHT.Name:
            gamepad.right_joystick_float(command.XValue, -command.YValue)
        elif command.AxisInput.Name == AxisTypes.RSB_TOP_DOWN.Name:
            gamepad.right_joystick_float(command.XValue, -command.YValue)
        elif command.AxisInput.Name == AxisTypes.LEFT_TRIGGER.Name:
            gamepad.left_trigger_float(command.XValue)
        elif command.AxisInput.Name == AxisTypes.RIGHT_TRIGGER.Name:
            gamepad.right_trigger_float(command.YValue)
        gamepad.update()

    def __handle_dpad_command(self, command: DpadInput, gamepad: VX360Gamepad):
        if command.Name == DpadTypes.TOP.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        elif command.Name == DpadTypes.DOWN.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        elif command.Name == DpadTypes.LEFT.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        elif command.Name == DpadTypes.RIGHT.Name:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        elif command.Name == DpadTypes.RELEASE_TOP.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        elif command.Name == DpadTypes.RELEASE_DOWN.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        elif command.Name == DpadTypes.RELEASE_LEFT.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        elif command.Name == DpadTypes.RELEASE_RIGHT.Name:
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        gamepad.update()

    def __close_connection_with_socket(self, client_socket, log_message="", remove_socket=True):
        if log_message != "":
            self.__print(log_message)
        client_socket.close()
        if remove_socket:
            del self.__socket_inputs[client_socket]

    def __shutdown_connection_with_socket(self, client_socket, log_message="", remove_socket=True):
        if log_message != "":
            self.__print(log_message)
        client_socket.shutdown(socket.SHUT_RDWR)
        if remove_socket:
            del self.__socket_inputs[client_socket]
