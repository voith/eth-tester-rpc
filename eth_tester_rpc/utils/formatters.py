from .toolz import (
    curry,
)


@curry
def apply_formatter_if(condition, formatter, value):
    if condition(value):
        return formatter(value)
    else:
        return value
