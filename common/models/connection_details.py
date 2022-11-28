import json


class ConnectionDetails:

    def __init__(self, name: str):
        self.__name = name

    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, value):
        self.__name = value

    def __iter__(self):
        yield from {
            "name": str(self.__name),
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

        return ConnectionDetails(json_map["name"])

    def validate(self) -> bool:
        if len(self.__name) > 40:
            return False
        return True
