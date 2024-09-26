from enum import Enum


class Color(Enum):
    BLACK = [0, 0, 0]
    BLUE = [255, 0, 0]
    GREEN = [0, 255, 0]
    RED = [0, 0, 255]
    CYAN = [255, 255, 0]
    MAGENTA = [255, 0, 255]
    YELLOW = [0, 255, 255]
    WHITE = [255, 255, 255]

    DEFAULT_VALUE = [170, 255, 0]
    HIGHLIGHTED_VALUE = [255, 0, 170]
    LOW_VALUE = [255, 178, 102]
    MEDIUM_VALUE = [153, 255, 153]
    HIGH_VALUE = [0, 150, 255]
    INSANE_VALUE = [178, 102, 255]
