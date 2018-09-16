try:
    from cytoolz import (
        compose,
        curry,
        excepts,
    )
except ImportError:
    from toolz import (  # noqa: F401
        compose,
        curry,
        excepts,
    )
