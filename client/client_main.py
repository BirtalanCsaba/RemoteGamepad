import json
import socket
import pygame
from pygame import JOYBUTTONUP, JOYAXISMOTION, JOYBUTTONDOWN, JOYHATMOTION

from client.controller_input import get_controller_button_type, get_controller_dpad_type, get_controller_axis_type, \
    get_controller_button_release_type, is_controller_release_dpad_type, get_controller_dpad_release_by_dpad_input
from common.connection_details import PORT
from common.models.axis_input_value import AxisInputValue
from common.models.axis_types import AxisTypes
from common.models.controllerinput import ControllerInput
from common.models.dpad_input import DpadInput

joysticks = []
clock = pygame.time.Clock()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
keepPlaying = True
addr = ("127.0.0.1", PORT)

last_dpad_type: DpadInput
last_left_trigger_value = 0.0
last_right_trigger_value = 0.0

SEPARATOR = "\r\n"


def init_server_connection():
    global client_socket
    # client_socket.connect(addr)


def init_controller_detection():
    pygame.init()
    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    print("Detected joystick " + joysticks[-1].get_name() + "'")


def handle_controller_input():
    global last_dpad_type, last_left_trigger_value, last_right_trigger_value

    while keepPlaying:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == JOYBUTTONDOWN:
                button_type = get_controller_button_type(event.button)
                send_input(button_type)
                # print(button_type)
            elif event.type == JOYAXISMOTION:
                axis_type = get_controller_axis_type(event.axis)
                if axis_type == AxisTypes.LSB_LEFT_RIGHT or axis_type == AxisTypes.LSB_TOP_DOWN:
                    x_value = joysticks[-1].get_axis(0)
                    y_value = joysticks[-1].get_axis(1)
                elif axis_type == AxisTypes.RSB_TOP_DOWN or axis_type == AxisTypes.RSB_TOP_DOWN:
                    x_value = joysticks[-1].get_axis(2)
                    y_value = joysticks[-1].get_axis(3)
                elif axis_type == AxisTypes.LEFT_TRIGGER:
                    x_value = joysticks[-1].get_axis(4)
                    y_value = 0.0
                    if x_value < -0.2:
                        x_value = 0.0
                    if last_left_trigger_value == 0.0 and x_value == 0.0:
                        continue
                    if x_value == 0.0:
                        axis_value = AxisInputValue(axis_type, x_value, y_value)
                        send_input(axis_value)
                    last_left_trigger_value = x_value
                else:
                    x_value = 0.0
                    y_value = joysticks[-1].get_axis(5)
                    if y_value < -0.2:
                        y_value = 0.0
                    if last_right_trigger_value == 0.0 and y_value == 0.0:
                        continue
                    if y_value == 0.0:
                        axis_value = AxisInputValue(axis_type, x_value, y_value)
                        send_input(axis_value)
                    last_right_trigger_value = y_value
                if abs(x_value) < 0.1:
                    x_value = 0.0
                if abs(y_value) < 0.1:
                    y_value = 0.0
                axis_value = AxisInputValue(axis_type, x_value, y_value)

                send_input(axis_value)
                # print(axis_value)
            elif event.type == JOYHATMOTION:
                # print(event)
                if is_controller_release_dpad_type(event.value) and last_dpad_type is not None:
                    dpad_type = get_controller_dpad_release_by_dpad_input(last_dpad_type)
                else:
                    dpad_type = get_controller_dpad_type(event.value)
                    last_dpad_type = dpad_type

                send_input(dpad_type)
                # print(dpad_type)
            elif event.type == JOYBUTTONUP:
                dpad_release_type = get_controller_button_release_type(event.button)
                send_input(dpad_release_type)
                # print(dpad_release_type)
        clock.tick(20)


def send_input(controller_input: ControllerInput):
    global SEPARATOR
    if controller_input is None:
        return
    json_str = controller_input.to_json()
    client_socket.sendto(json_str.encode('utf-8'), addr)


if __name__ == '__main__':
    init_server_connection()
    init_controller_detection()
    handle_controller_input()
