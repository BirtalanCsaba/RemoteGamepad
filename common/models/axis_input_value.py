import json

from common.models.axis_input import AxisInput
from common.models.controllerinput import ControllerInput


class AxisInputValue(ControllerInput):
    input_type = "axis"

    def __init__(self, axis_input: AxisInput, x_value: float, y_value: float):
        self.__axis_input = axis_input
        self.__x_value = x_value
        self.__y_value = y_value

    @property
    def AxisInput(self):
        return self.__axis_input

    @property
    def XValue(self):
        return self.__x_value

    @XValue.setter
    def XValue(self, value):
        self.__x_value = value

    @property
    def YValue(self):
        return self.__y_value

    @YValue.setter
    def YValue(self, value):
        self.__y_value = value

    def __iter__(self):
        yield from {
            "input_type": self.input_type,
            "axis_input": str(self.__axis_input),
            "x_value": self.__x_value,
            "y_value": self.__y_value,
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self) -> str:
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        return AxisInputValue(AxisInput.from_json(json.loads(json_dct["axis_input"])),
                              json_dct["x_value"],
                              json_dct["y_value"])
