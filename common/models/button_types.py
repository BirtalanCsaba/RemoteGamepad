from common.models.button_input import ButtonInput


class ButtonTypes:
    A = ButtonInput("A", 0)
    B = ButtonInput("B", 1)
    X = ButtonInput("X", 2)
    Y = ButtonInput("Y", 3)
    LEFT_BUTTON = ButtonInput("LEFT_TRIGGER", 4)
    RIGHT_BUTTON = ButtonInput("RIGHT_TRIGGER", 5)
    RELEASE_A = ButtonInput("RELEASE_A", 0)
    RELEASE_B = ButtonInput("RELEASE_B", 1)
    RELEASE_X = ButtonInput("RELEASE_X", 2)
    RELEASE_Y = ButtonInput("RELEASE_Y", 3)
    RELEASE_LEFT_BUTTON = ButtonInput("RELEASE_LEFT_TRIGGER", 4)
    RELEASE_RIGHT_BUTTON = ButtonInput("RELEASE_RIGHT_TRIGGER", 5)

    ALL_INPUTS = [
        A,
        B,
        X,
        Y,
        LEFT_BUTTON,
        RIGHT_BUTTON,
    ]

    RELEASE_INPUTS = [
        RELEASE_A,
        RELEASE_B,
        RELEASE_X,
        RELEASE_Y,
        RELEASE_LEFT_BUTTON,
        RELEASE_RIGHT_BUTTON,
    ]
