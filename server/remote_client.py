from vgamepad import VX360Gamepad


class RemoteClient:
    def __init__(self, address: str | None, name: str | None, is_connected=False, gamepad: VX360Gamepad | None = None):
        self.__address = address
        self.__name = name
        self.__is_connected = is_connected
        self.__gamepad = gamepad

    @property
    def Address(self):
        return self.__address

    @Address.setter
    def Address(self, value):
        self.__address = value

    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, value):
        self.__name = value

    @property
    def IsConnected(self):
        return self.__is_connected

    @IsConnected.setter
    def IsConnected(self, value):
        self.__is_connected = value

    @property
    def Gamepad(self):
        return self.__gamepad

    @Gamepad.setter
    def Gamepad(self, value):
        self.__gamepad = value

    def __str__(self):
        return f"RemoteClient(address: {self.__address}, name: {self.__name}, isConnected: {self.__is_connected})"
