import json

from common.models.controllerinput import ControllerInput


class AxisInput(ControllerInput):
    def __init__(self, name: str, axis: int):
        self.__name = name
        self.__axis = axis

    @property
    def Name(self):
        return self.__name

    @property
    def Axis(self):
        return self.__axis

    def __iter__(self):
        yield from {
            "name": str(self.__name),
            "axis": str(self.__axis),
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self) -> str:
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        return AxisInput(json_dct['name'], json_dct["axis"])





