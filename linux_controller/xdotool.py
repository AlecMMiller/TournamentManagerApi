from . import terminal
import time

LEFT_MOUSE = 1
RIGHT_MOUSE = 3

MOUSE_LEFT_KEY = 'Pointer_Button_1'
MOUSE_RIGHT_KEY = 'Pointer_Button_3'


def __xdotool_command(arguments):
    return terminal.run(['xdotool'] + arguments)


def mouse_move(x, y):
    cmd = ['mousemove', str(x), str(y)]
    __xdotool_command(cmd)


def click(right=False):
    if right:
        mouse = RIGHT_MOUSE
    else:
        mouse = LEFT_MOUSE
    cmd = ['click', str(mouse)]
    __xdotool_command(cmd)


def click_at(x, y, right=False):
    mouse_move(x, y)
    click(right=right)
    time.sleep(0.1)


def get_window_by_name(name):
    cmd = ['search', '--name', name]
    ret = __xdotool_command(cmd)
    try:
        value = int(ret)
        return value
    except ValueError:
        raise ValueError("Window " + name + "not found")


def get_window_by_click():
    cmd = ['selectwindow']
    ret = __xdotool_command(cmd)

    return int(ret)


def get_window_name(window):
    cmd = ['getwindowname', str(window)]
    ret = __xdotool_command(cmd)
    ret = ret.decode('UTF-8').strip()
    return ret


def get_name_by_click():
    window = get_window_by_click()
    name = get_window_name(window)
    return name


def move_window(window, x, y):
    cmd = ['windowmove', str(window), str(x), str(y)]
    __xdotool_command(cmd)


def resize_window(window, x, y):
    cmd = ['windowsize', str(window), str(x), str(y)]
    __xdotool_command(cmd)
