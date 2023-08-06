# ANSIEnum

### ANSIEnum: Python escape codes made easy!

Want a simple way to put ANSI escape codes in another project?

So did I! So here is my solution...

## Description

Allows inline adding of ANSI color codes and cursor manipulation

## Features

- [SGR](https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences) properties for
  setting text FG/BG color and effects (can also be added together)
- [CSI](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters) functions for cursor
  manipulation, properties for clearing screen by Line or Display

## Installation

```shell
$ pip install ansienum
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
print(f"ANSI.cursor_up(2)Moved text")
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

### Examples

Using f-strings (Python 3.6+)

![f-string usage](.README_images/usage_1.png)

Using % formatting

![% usage](.README_images/usage_2.png)

Multi-formatting with cursor position

![](.README_images/usage_cursor.png)

## Contributing

If you are reading this and want to contribute, please feel free to create an issue. Note that it is a work in progress
and things probably will change, but I intend to keep backward compatibility where possible.

## License

This project is under an [MIT license](LICENSE)

#### (c) 2021 Paul Taylor   @paulyt