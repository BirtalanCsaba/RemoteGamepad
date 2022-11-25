from common.models.axis_input import AxisInput


class AxisTypes:
    LSB_LEFT_RIGHT = AxisInput("LSB_LEFT_RIGHT", 0)
    LSB_TOP_DOWN = AxisInput("LSB_TOP_DOWN", 1)
    RSB_LEFT_RIGHT = AxisInput("RSB_LEFT_RIGHT", 2)
    RSB_TOP_DOWN = AxisInput("RSB_TOP_DOWN", 3)
    LEFT_TRIGGER = AxisInput("LEFT_TRIGGER", 4)
    RIGHT_TRIGGER = AxisInput("RIGHT_TRIGGER", 5)

    ALL_INPUTS = [
        LSB_TOP_DOWN,
        LSB_LEFT_RIGHT,
        RSB_TOP_DOWN,
        RSB_LEFT_RIGHT,
        LEFT_TRIGGER,
        RIGHT_TRIGGER
    ]
