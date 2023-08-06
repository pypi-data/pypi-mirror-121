"""
ANSIEnum: Python escape codes made easy!

(c) 2021 Paul Taylor   @paulyt
under MIT license

Reference: https://en.wikipedia.org/wiki/ANSI_escape_code

Usage:

from ansienum import ANSI

# Simple text color with f-strings:
print(f"{ANSI.FG_RED}Red text!{ANSI.RESET}")

# Codes of the same type can be added:
print(f"{ANSI.FG_RED+ANSI.BG_BLUE}Red on blue text!{ANSI.RESET}")

# Move cursor:
print(f"ANSI.cursor_up(2)Moved text")

-------------------------------------------

# Cursor functions:
ANSI.cursor_at(n, m)
ANSI.cursor_up(n)
ANSI.cursor_down(n)
ANSI.cursor_right(n)
ANSI.cursor_left(n)
ANSI.cursor_next_line(n)
ANSI.cursor_prev_line(n)
ANSI.cursor_horiz_abs(n)
"""
from enum import Enum
from typing import Union

__all__ = ["ANSI"]

VERSION = 0.2


class ANSIEnum(Enum):
    def __init__(self, n: Union[int, list[int]], control_byte: str, abbr: str = None, description: str = None):
        self._n = n
        if type(self._n) is list:
            for i, t in enumerate(self._n):
                if type(t) is not int:
                    raise TypeError(
                        "%s sequence item %d: expected int instance, %s found" % (
                            n, i, type(t).__name__))
        elif type(self._n) is not int:
            raise TypeError("'%s': expected int instance, %s found" % (self._n, type(self._n).__name__))
        self._control_byte = control_byte
        self._abbr = None
        if abbr is not None:
            self._abbr = abbr
        if control_byte == "m":
            self._abbr = "SGR"
        elif self._abbr is None:
            self._abbr = "CSI"
        self._description = description

    @property
    def _n_str(self):
        if type(self._n) is list:
            return ';'.join([str(n) for n in self._n])
        else:
            return str(self._n)

    @property
    def info(self):
        info = "%s (%s):  'ESC[%s%s'" % (self.name, self._abbr, self._n_str, self._control_byte)
        if self._description:
            info += "  | %s" % self._description
        return info

    def __add__(self, other):
        if self.value[1] != "m" or other.value[1] != "m":
            raise TypeError(
                "unsupported operand code(s) for +: '%s' and '%s'" % (self.value[1], other.value[1]))
        self_n, self_code = self.value
        other_n, other_code = other.value
        new_name = "%s+%s" % (self.name, other.name)
        if type(self_n) is list:
            new_n = self_n
            if other_n not in self_n:
                new_n.append(other_n)
        else:
            new_n = [self_n, other_n]
        return getattr(ANSIEnum("ANSI", {new_name: (new_n, self._control_byte)}), new_name)

    def __str__(self):
        return "\x1b[%s%s" % (self._n_str, self._control_byte)

    def __repr__(self):
        return "%s%s" % (self._n_str, self._control_byte)


ANSI = ANSIEnum("ANSI", {
    # CSI (Control Sequence Introducer) sequences
    "CUR_UP_1": (1, "A", "CUU"),
    "cursor_up": lambda n=1: getattr(
        ANSIEnum("ANSI", {"CUR_UP_%d" % n: (n, "A", "CUU", "Move cursor up %d line(s)" % n)}),
        "CUR_UP_%d" % n),
    "CUR_DOWN_1": (1, "B", "CUD"),
    "cursor_down": lambda n=1: getattr(
        ANSIEnum("ANSI", {"CUR_DOWN_%d" % n: (n, "B", "CUD", "Move cursor down %d line(s)" % n)}),
        "CUR_DOWN_%d" % n),
    "CUR_FWD_1": (1, "C", "CUF"),
    "cursor_right": lambda n=1: getattr(
        ANSIEnum("ANSI", {"CUR_FWD_%d" % n: (n, "C", "CUF", "Move cursor right %d column(s)" % n)}),
        "CUR_FWD_%d" % n),
    "CUR_BACK_1": (1, "D", "CUB"),
    "cursor_left": lambda n=1: getattr(
        ANSIEnum("ANSI", {"CUR_BACK_%d" % n: (n, "D", "CUB", "Move cursor left %d column(s)" % n)}),
        "CUR_BACK_%d" % n),
    "CUR_NEXT_LINE": (1, "E", "CNL"),
    "cursor_next_line": lambda n=1: getattr(
        ANSIEnum("ANSI", {"CUR_NEXT_LINE_%d" % n: (n, "E", "CNL", "Move cursor to first column, %d line(s) down" % n)}),
        "CUR_NEXT_LINE_%d" % n),
    "CUR_PREV_LINE": (1, "F", "CPL"),
    "cursor_prev_line": lambda n=1: getattr(
        ANSIEnum("ANSI", {"CUR_PREV_%d" % n: (n, "F", "CPL", "Move cursor to first column, %d line(s) up" % n)}),
        "CUR_PREV_%d" % n),
    "CUR_HOR_ABS": (1, "G", "CHA", "Cursor Horizontal Absolute, column 1"),
    "cursor_horiz_abs": lambda n=1: getattr(
        ANSIEnum("ANSI", {"CUR_HOR_ABS_%d" % n: (n, "G", "CHA", "Move cursor to column %d" % n)}),
        "CUR_HOR_ABS_%d" % n),
    "cursor_at": lambda n=1, m=1: getattr(
        ANSIEnum("ANSI", {"CUR_AT_%d_%d" % (n, m): ([n, m], "H", "CUP", "Move cursor to row %d, column %d" % (n, m))}),
        "CUR_AT_%d_%d" % (n, m)),

    "ERASE_DISP_RIGHT": (0, "J", "EID", "Erase in Display, Cursor to end of screen"),
    "ERASE_DISP_LEFT": (1, "J", "EID", "Erase in Display, Start of screen to cursor"),
    "ERASE_DISP_ALL": (2, "J", "EID", "Erase in Display, Entire screen (preserve scrollback)"),
    "ERASE_DISP_ALLSB": (3, "J", "EID", "Erase in Display, Entire screen including scrollback"),
    "ERASE_LINE_RIGHT": (0, "K", "EIL", "Erase in Line, Cursor up to end"),
    "ERASE_LINE_LEFT": (1, "K", "EIL", "Erase in Line, Start up to cursor"),
    "ERASE_LINE_ALL": (2, "K", "EIL", "Erase in Line, Entire line"),

    # SGR (Select Graphic Rendition) parameters
    "RESET": (0, "m"),
    "ITAL_ON": (3, "m"),
    "UL_ON": (4, "m"),
    "BLINK_SLOW": (5, "m"),
    "BLINK_FAST": (6, "m"),
    "INVERT_ON": (7, "m"),
    "STRIKE_ON": (9, "m"),
    "ITAL_OFF": (23, "m"),
    "UL_OFF": (24, "m"),
    "BLINK_OFF": (25, "m"),
    "INVERT_OFF": (27, "m"),
    "STRIKE_OFF": (29, "m"),
    "FG_BLACK": (30, "m"),
    "FG_RED": (31, "m"),
    "FG_GREEN": (32, "m"),
    "FG_YELLOW": (33, "m"),
    "FG_BLUE": (34, "m"),
    "FG_MAGENTA": (35, "m"),
    "FG_CYAN": (36, "m"),
    "FG_WHITE": (37, "m"),
    "FG_DEFAULT": (39, "m"),
    "FG_GRAY": (90, "m"),
    "FG_BR_RED": (91, "m"),
    "FG_BR_GREEN": (92, "m"),
    "FG_BR_YELLOW": (93, "m"),
    "FG_BR_BLUE": (94, "m"),
    "FG_BR_MAGENTA": (95, "m"),
    "FG_BR_CYAN": (96, "m"),
    "FG_BR_WHITE": (97, "m"),
    "BG_BLACK": (40, "m"),
    "BG_RED": (41, "m"),
    "BG_GREEN": (42, "m"),
    "BG_YELLOW": (43, "m"),
    "BG_BLUE": (44, "m"),
    "BG_MAGENTA": (45, "m"),
    "BG_CYAN": (46, "m"),
    "BG_WHITE": (47, "m"),
    "BG_DEFAULT": (49, "m"),
    "BG_GRAY": (100, "m"),
    "BG_BR_RED": (101, "m"),
    "BG_BR_GREEN": (102, "m"),
    "BG_BR_YELLOW": (103, "m"),
    "BG_BR_BLUE": (104, "m"),
    "BG_BR_MAGENTA": (105, "m"),
    "BG_BR_CYAN": (106, "m"),
    "BG_BR_WHITE": (107, "m"),
})
