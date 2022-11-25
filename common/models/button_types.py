from common.models.button_input import ButtonInput


class ButtonTypes:
    A = ButtonInput("A", 0)
    B = ButtonInput("B", 1)
    X = ButtonInput("X", 2)
    Y = ButtonInput("Y", 3)
    LEFT_BUTTON = ButtonInput("LEFT_BUTTON", 4)
    RIGHT_BUTTON = ButtonInput("RIGHT_BUTTON", 5)
    MENU = ButtonInput("MENU", 6)
    START = ButtonInput("START", 7)
    L3 = ButtonInput("L3", 8)
    R3 = ButtonInput("R3", 9)

    RELEASE_A = ButtonInput("RELEASE_A", 0)
    RELEASE_B = ButtonInput("RELEASE_B", 1)
    RELEASE_X = ButtonInput("RELEASE_X", 2)
    RELEASE_Y = ButtonInput("RELEASE_Y", 3)
    RELEASE_LEFT_BUTTON = ButtonInput("RELEASE_LEFT_BUTTON", 4)
    RELEASE_RIGHT_BUTTON = ButtonInput("RELEASE_RIGHT_BUTTON", 5)
    RELEASE_MENU = ButtonInput("RELEASE_MENU", 6)
    RELEASE_START = ButtonInput("RELEASE_START", 7)
    RELEASE_L3 = ButtonInput("RELEASE_L3", 8)
    RELEASE_R3 = ButtonInput("RELEASE_R3", 9)

    ALL_INPUTS = [
        A,
        B,
        X,
        Y,
        LEFT_BUTTON,
        RIGHT_BUTTON,
        MENU,
        START,
        L3,
        R3,
    ]

    RELEASE_INPUTS = [
        RELEASE_A,
        RELEASE_B,
        RELEASE_X,
        RELEASE_Y,
        RELEASE_LEFT_BUTTON,
        RELEASE_RIGHT_BUTTON,
        RELEASE_MENU,
        RELEASE_START,
        RELEASE_L3,
        RELEASE_R3
    ]
