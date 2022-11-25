import json

from common.models.axis_input import AxisInput
from common.models.controllerinput import ControllerInput


class AxisInputValue(ControllerInput):
    input_type = "axis"

    def __init__(self, axis_input: AxisInput, value: float):
        self.__axis_input = axis_input
        self.__value = value

    @property
    def AxisInput(self):
        return self.__axis_input

    @property
    def Value(self):
        return self.__value

    def __iter__(self):
        yield from {
            "input_type": self.input_type,
            "axis_input": str(self.__axis_input),
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
        return AxisInputValue(AxisInput.from_json(json.loads(json_dct["axis_input"])), json_dct["value"])
