from common.models.axis_types import AxisTypes
from common.models.button_types import ButtonTypes
from common.models.dpad_input import DpadInput
from common.models.dpad_types import DpadTypes


def get_controller_button_type(input_value):
    for btn_type in ButtonTypes.ALL_INPUTS:
        if btn_type.Value == input_value:
            return btn_type
    return None


def get_controller_button_release_type(input_value):
    for btn_type in ButtonTypes.RELEASE_INPUTS:
        if btn_type.Value == input_value:
            return btn_type
    return None


def is_controller_release_dpad_type(input_value):
    if DpadTypes.RELEASE.Value == input_value:
        return True
    return False


def get_controller_dpad_release_by_dpad_input(input_value: DpadInput):
    if input_value.Name == DpadTypes.TOP.Name:
        return DpadTypes.RELEASE_TOP
    elif input_value.Name == DpadTypes.DOWN.Name:
        return DpadTypes.RELEASE_DOWN
    elif input_value.Name == DpadTypes.LEFT.Name:
        return DpadTypes.RELEASE_LEFT
    elif input_value.Name == DpadTypes.RIGHT.Name:
        return DpadTypes.RELEASE_RIGHT
    return None


def get_controller_axis_type(input_axis):
    for axis_type in AxisTypes.ALL_INPUTS:
        if axis_type.Axis == input_axis:
            return axis_type
    return None


def get_controller_dpad_type(input_value):
    for dpad in DpadTypes.ALL_INPUTS:
        if dpad.Value == input_value:
            return dpad
    return None
