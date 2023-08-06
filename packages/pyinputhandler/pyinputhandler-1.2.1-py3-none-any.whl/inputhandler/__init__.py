import threading

from .getwch import getwch
from .buffer_input import Input, buffer_input
from .input_types import try_input, safe_input, safe_try_input
from . import input_types
from . import constant


def get_input_buffer():
    return buffer_input.get_input_buffer()


def get_safe_buffer():
    return safe_input.get_input_buffer()


def set_lock(lock):
    if not isinstance(lock, threading.Lock):
        raise TypeError("lock must be a threading.Lock instance")

    safe_input._input_lock = lock
    safe_try_input._input_lock = lock
    input_types.ThreadSafeInput._input_lock = lock
    input_types.ThreadSafeTryInput._input_lock = lock


def fix_cursor(input_=None):
    if isinstance(input_, Input):
        input_._move_cursor()
    elif isinstance(constant.CURRENT_INPUT, Input) or constant.CURRENT_INPUT is None:

        if constant.CURRENT_INPUT is not None:
            constant.CURRENT_INPUT._move_cursor()
    else:
        raise TypeError("the global constant 'CURRENT_INPUT' was reassigned")
