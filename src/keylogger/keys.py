from enum import Enum


class Key(Enum):
    F1 = 122
    F2 = 120
    F3 = 99
    F4 = 118
    F5 = 96  # undetectable by keylogger
    F6 = 97
    F7 = 98
    F8 = 100
    F9 = 101
    F10 = 109
    F11 = 103
    F12 = 111


class Modifier(Enum):
    CapsLock = 0x10000
    Shift = 0x20000
    Control = 0x40000
    Option = 0x80000
    Command = 0x100000
    Function = 0x800000
