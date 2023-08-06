# ANSIEnum: *Python + ANSI = easy!*

Q) Want a simple way to put ANSI escape codes in your project?

A) Yes? So did I! Here is my solution...

## Description

Allows inline adding of [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code) for color and cursor
manipulation.

## Features

- [SGR](https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences) properties for
  setting text **FG**/**BG** color (incl **BR**ight) plus effects (these can also be added together):
  - FG_*
  - FG_BR_*
  - BG_*
  - BG_BR_*
  - UL_, ITAL_, STRIKE_, INVERT_and BLINK_ control
- [CSI](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters) properties for
  clearing screen:
  - ERASE_DISP_*
  - ERASE_LINE_*
- CSI functions for cursor control (complete list [below](#Cursor functions)):
  - cursor_*

*Note:* Complete property (upper case) names are available from the enum with `dir(ANSI)`

## Installation

```shell
$ pip install ANSIEnum
```

## Usage

```python
from ansienum import ANSI

# Simple text color with f-strings:
print(f"{ANSI.FG_RED}Red text!{ANSI.RESET}")

# Codes of the same type can be added:
my_color = ANSI.FG_RED + ANSI.BG_BLUE
print(f"{my_color}Red on blue text!{ANSI.RESET}")

# Move cursor:
print(f"{ANSI.cursor_up(2)}Moved text")
```

### Cursor functions

```python
ANSI.cursor_at(n, m)
ANSI.cursor_up(n)
ANSI.cursor_down(n)
ANSI.cursor_right(n)
ANSI.cursor_left(n)
ANSI.cursor_next_line(n)
ANSI.cursor_prev_line(n)
ANSI.cursor_horiz_abs(n)
```

## Contributing

If you are reading this and want to contribute, please feel free to create an issue. Note that it is a work in progress
and things probably will change, but I intend to keep backward compatibility where possible.

## License

This project is under an [MIT license](LICENSE)

#### (c) 2021 Paul Taylor   @paulyt