from server.socket_controller import SocketController


class Command:
    def __init__(self, message: str, command_function):
        self.__message = message
        self.__command_function = command_function

    @property
    def Message(self):
        return self.__message

    @Message.setter
    def Message(self, value):
        self.__message = value

    @property
    def CommandFunction(self):
        return self.__command_function

    @CommandFunction.setter
    def CommandFunction(self, value):
        self.__command_function = value


class ServerUi:
    def __init__(self):
        self.__max_players = 1
        self.__port = 12000
        self.__command_list = {
            "0": Command("Exit", self.__application_exit),
            "1": Command("Settings", self.__settings),
            "2": Command("Show settings", self.__show_settings),
            "3": Command("Start server", self.__start_server),
        }

    def application_startup(self):
        finished = False
        while not finished:
            self.__print_options()
            command = input("command: ")
            if command in self.__command_list:
                self.__command_list[command].CommandFunction()
            else:
                print("Bad command!\n")

    def __application_exit(self):
        quit()

    def __print_options(self):
        print("====== Menu ======")
        for command in self.__command_list.keys():
            print(f"{command}: {self.__command_list[command].Message}")

    def __settings(self):
        try:
            max_players = int(input("Maximum number of players (from 1 to 3): "))
            if 1 < max_players > 3:
                print("Invalid number of players")
                return
            self.__max_players = max_players

            port = int(input("Server port: "))
            if 1 < port > 65535:
                print("Out of range")
                return
            self.__port = port
        except Exception:
            print("Invalid input")

    def __show_settings(self):
        print(f"Maximum number of players allowed to join: {self.__max_players}")
        print(f"Server port: {self.__port}")

    def __start_server(self):
        socket_controller = SocketController(self.__max_players, self.__port)
        socket_controller.start_listen()

