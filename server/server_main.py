import json

import vgamepad as vg
import socket

from vgamepad import XUSB_BUTTON

from common.connection_details import PORT
from common.models.axis_input_value import AxisInputValue
from common.models.axis_types import AxisTypes
from common.models.button_input import ButtonInput
from common.models.button_types import ButtonTypes
from common.models.dpad_input import DpadInput
from common.models.dpad_types import DpadTypes

gamepad = vg.VX360Gamepad()


def handle_button_command(command: ButtonInput):
    global gamepad

    if command.Name == ButtonTypes.A.Name:
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
    elif command.Name == ButtonTypes.B.Name:
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
    elif command.Name == ButtonTypes.X.Name:
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
    elif command.Name == ButtonTypes.Y.Name:
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
    elif command.Name == ButtonTypes.RELEASE_LEFT_BUTTON.Name:
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    elif command.Name == ButtonTypes.RELEASE_RIGHT_BUTTON.Name:
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
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
    gamepad.update()


def handle_axis_command(command: AxisInputValue):
    global gamepad

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


def handle_dpad_command(command: DpadInput):
    global gamepad

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


class Buffer:

    def __init__(self, sock):
        self.sock = sock
        self.buffer = b''

    def get_line(self):
        while b'\r\n' not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                # socket closed
                return None
            self.buffer += data
        line, sep, self.buffer = self.buffer.partition(b'\r\n')
        return line.decode()


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', PORT))
    # server_socket.listen()
    # conn, addr = server_socket.accept()

    remaining_buffer = ""

    # with conn:
    while True:
        # # buffer = Buffer(conn)
        # bytes_message = buffer.get_line()
        # if bytes_message is None:
        #     continue
        # # print(bytes_message)
        # if remaining_buffer != "":
        #     print()
        #     print(remaining_buffer)
        #     print()
        #     remaining_buffer += bytes_message
        #     bytes_message = str(remaining_buffer)
        #     remaining_buffer = ""
        bytes_message, addr = server_socket.recvfrom(1024)

        try:
            message = json.loads(bytes_message.decode('utf-8'))
            print(message)
        except Exception:
            remaining_buffer += bytes_message
            continue

        if message["input_type"] == "button":
            button_command = ButtonInput.from_json(message)
            handle_button_command(button_command)
            # print("button")
        elif message["input_type"] == "axis":
            axis_command = AxisInputValue.from_json(message)
            handle_axis_command(axis_command)
            # print("axis")
        elif message["input_type"] == "dpad":
            dpad_command = DpadInput.from_json(message)
            handle_dpad_command(dpad_command)
            # print("dpad")
