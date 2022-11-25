from common.models.dpad_input import DpadInput


class DpadTypes:
    LEFT = DpadInput("LEFT", (-1, 0))
    RIGHT = DpadInput("RIGHT", (1, 0))
    TOP = DpadInput("TOP", (0, 1))
    DOWN = DpadInput("DOWN", (0, -1))
    RELEASE = DpadInput("RELEASE", (0, 0))
    RELEASE_LEFT = DpadInput("RELEASE_LEFT", (0, 0))
    RELEASE_RIGHT = DpadInput("RELEASE_RIGHT", (0, 0))
    RELEASE_TOP = DpadInput("RELEASE_TOP", (0, 0))
    RELEASE_DOWN = DpadInput("RELEASE_DOWN", (0, 0))

    ALL_INPUTS = [
        LEFT,
        RIGHT,
        TOP,
        DOWN
    ]
