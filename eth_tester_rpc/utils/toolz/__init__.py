try:
    from cytoolz import (
        compose,
        curry,
        excepts,
    )
except ImportError:
    from toolz import (
        compose,
        curry,
        excepts,
    )
