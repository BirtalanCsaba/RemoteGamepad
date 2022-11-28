import json


class ConnectionResponseStatus:
    EXIT = "exit"


class ConnectionResponse:
    def __init__(self, value: str):
        self.__value = value

    @property
    def Name(self):
        return self.__value

    @Name.setter
    def Name(self, value):
        self.__value = value

    def __iter__(self):
        yield from {
            "name": str(self.__value),
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(message: str):
        try:
            json_map = json.loads(message)
        except Exception:
            raise Exception("Cannot convert from json")
        if "name" not in json_map:
            raise Exception("Json fields not found")

        return ConnectionResponse(json_map["name"])

    def validate(self) -> bool:
        if len(self.__value) > 40:
            return False
        return True
