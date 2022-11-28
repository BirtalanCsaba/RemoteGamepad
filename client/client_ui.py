from client.client_controller import ClientController


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


class ClientUi:
    def __init__(self):
        self.__name = "Remote player"
        self.__port = 12000
        self.__server_address = "127.0.0.1"
        self.__command_list = {
            "0": Command("Exit", self.__application_exit),
            "1": Command("Settings", self.__settings),
            "2": Command("Show settings", self.__show_settings),
            "3": Command("Connect", self.__connect),
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
            name = input("name: ")
            if len(name) > 40:
                print("Cannot set name. Reason: too long.")
            else:
                self.__name = name

            self.__server_address = input("server address: ")

            port = int(input("Server port: "))
            if 1 < port > 65535:
                print("Out of range")
                return
            self.__port = port
        except Exception:
            print("Invalid input")

    def __show_settings(self):
        print(f"Name: {self.__name}")
        print(f"Connection port: {self.__port}")

    def __connect(self):
        client_controller = ClientController(self.__port, self.__server_address, self.__name)
        client_controller.start_connection()
