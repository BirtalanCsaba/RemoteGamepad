import socket
from threading import Thread

import pygame
import select
from pygame import JOYBUTTONUP, JOYAXISMOTION, JOYBUTTONDOWN, JOYHATMOTION

from client.controller_input import get_controller_button_type, get_controller_dpad_type, get_controller_axis_type, \
    get_controller_button_release_type, is_controller_release_dpad_type, get_controller_dpad_release_by_dpad_input
from common.models.axis_input_value import AxisInputValue
from common.models.axis_types import AxisTypes
from common.models.connection_details import ConnectionDetails
from common.models.connection_response import ConnectionResponse, ConnectionResponseStatus
from common.models.controller_input import ControllerInput
from common.models.dpad_input import DpadInput


class ClientController:
    __joysticks = []
    __clock = pygame.time.Clock()
    __client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    __last_dpad_type: DpadInput | None = None
    __last_left_trigger_value = 0.0
    __last_right_trigger_value = 0.0

    def __init__(self, port, server_address, name):
        self.__port = port
        self.__server_address = server_address
        self.__name = name
        self.__socket_inputs = []
        self.__finished = False
        self.__server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_connection(self):
        server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_tcp_socket.connect((self.__server_address, self.__port))
        except socket.error:
            print("Connecting to server failed.")
            return

        keyboard_input = Thread(target=self.__read_keyboard)
        keyboard_input.daemon = True
        keyboard_input.start()

        connection_details = ConnectionDetails(self.__name)
        server_tcp_socket.sendall(connection_details.to_json().encode('utf-8'))

        controller_input = Thread(target=self.__controller_handle)
        controller_input.start()

        print("Successfully connected to server!")
        print("Type q to quit the session")

        while not self.__finished:
            try:
                read_sockets, write_sockets, error_sockets = select.select(
                    [server_tcp_socket],
                    [],
                    [],
                    0
                )
            except select.error:
                server_tcp_socket.shutdown(2)
                server_tcp_socket.close()
                print('connection error')
                break
            for sock in read_sockets:
                if sock == server_tcp_socket:
                    self.__handle_server_response(sock)

        server_tcp_socket.close()
        keyboard_input.join()

    def __init_controller_detection(self):
        pygame.init()
        for i in range(0, pygame.joystick.get_count()):
            self.__joysticks.append(pygame.joystick.Joystick(i))
        self.__joysticks[-1].init()
        print("Detected joystick " + self.__joysticks[-1].get_name() + "'")

    def __controller_handle(self):
        self.__init_controller_detection()
        while not self.__finished:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == JOYBUTTONDOWN:
                    button_type = get_controller_button_type(event.button)
                    self.__send_input(button_type)
                    # print(button_type)
                elif event.type == JOYAXISMOTION:
                    axis_type = get_controller_axis_type(event.axis)
                    if axis_type == AxisTypes.LSB_LEFT_RIGHT or axis_type == AxisTypes.LSB_TOP_DOWN:
                        x_value = self.__joysticks[-1].get_axis(0)
                        y_value = self.__joysticks[-1].get_axis(1)
                    elif axis_type == AxisTypes.RSB_LEFT_RIGHT or axis_type == AxisTypes.RSB_TOP_DOWN:
                        x_value = self.__joysticks[-1].get_axis(2)
                        y_value = self.__joysticks[-1].get_axis(3)
                    elif axis_type == AxisTypes.LEFT_TRIGGER:
                        x_value = self.__joysticks[-1].get_axis(4)
                        y_value = 0.0
                        if x_value < -0.1:
                            x_value = 0.0
                        if self.__last_left_trigger_value == 0.0 and x_value == 0.0:
                            continue
                        if x_value == 0.0:
                            axis_value = AxisInputValue(axis_type, x_value, y_value)
                            self.__send_input(axis_value)
                        self.__last_left_trigger_value = x_value
                    elif axis_type == AxisTypes.RIGHT_TRIGGER:
                        x_value = 0.0
                        y_value = self.__joysticks[-1].get_axis(5)
                        if y_value < -0.1:
                            y_value = 0.0
                        if self.__last_right_trigger_value == 0.0 and y_value == 0.0:
                            continue
                        if y_value == 0.0:
                            axis_value = AxisInputValue(axis_type, x_value, y_value)
                            self.__send_input(axis_value)
                        self.__last_right_trigger_value = y_value
                    else:
                        continue

                    if abs(x_value) < 0.05:
                        x_value = 0.0
                    if abs(y_value) < 0.05:
                        y_value = 0.0

                    axis_value = AxisInputValue(axis_type, x_value, y_value)

                    self.__send_input(axis_value)

                    # print(axis_value)
                elif event.type == JOYHATMOTION:
                    # print(event)
                    if is_controller_release_dpad_type(event.value) and self.__last_dpad_type is not None:
                        dpad_type = get_controller_dpad_release_by_dpad_input(self.__last_dpad_type)
                    else:
                        dpad_type = get_controller_dpad_type(event.value)
                        self.__last_dpad_type = dpad_type

                    self.__send_input(dpad_type)
                    # print(dpad_type)
                elif event.type == JOYBUTTONUP:
                    dpad_release_type = get_controller_button_release_type(event.button)
                    self.__send_input(dpad_release_type)
                    # print(dpad_release_type)
            self.__clock.tick(20)

    def __send_input(self, controller_input: ControllerInput):
        if controller_input is None:
            return
        json_str = controller_input.to_json()
        print(json_str)
        self.__server_udp_socket.sendto(json_str.encode('utf-8'), (self.__server_address, self.__port))

    def __handle_server_response(self, sock):
        data = sock.recv(1024)
        if not data:
            print("Connection to the server lost. Press q to exit.")
            self.__finished = True
            return
        message = data.decode('uft-8')
        print(message)
        response = ConnectionResponse.from_json(message)
        if response == ConnectionResponseStatus.EXIT:
            self.__finished = True

    def __read_keyboard(self):
        while not self.__finished:
            quit_command = input()
            if quit_command == 'q':
                self.__finished = True
