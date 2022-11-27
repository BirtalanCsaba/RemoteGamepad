class RemoteClient:
    def __init__(self, address: str, name: str):
        self.__address = address
        self.__name = name

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
