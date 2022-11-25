import json

from common.models.controllerinput import ControllerInput


class ButtonInput(ControllerInput):
    input_type = "button"

    def __init__(self, name: str, value: int):
        self.__name = name
        self.__value = value

    @property
    def Name(self):
        return self.__name

    @property
    def Value(self):
        return self.__value

    def __iter__(self):
        yield from {
            "input_type": self.input_type,
            "name": str(self.__name),
            "value": self.__value
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self) -> str:
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        return ButtonInput(json_dct["name"], json_dct["value"])
