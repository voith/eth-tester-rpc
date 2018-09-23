import codecs

from eth_utils import (
    is_bytes,
    is_string,
    is_text,
)


def force_text(value):
    if is_text(value):
        return value
    elif is_bytes(value):
        return codecs.decode(value, "iso-8859-1")
    else:
        raise TypeError("Unsupported type: {0}".format(type(value)))


def force_obj_to_text(obj, skip_unsupported=False):
    if is_string(obj):
        return force_text(obj)
    elif isinstance(obj, dict):
        return {
            k: force_obj_to_text(v, skip_unsupported) for k, v in obj.items()
        }
    elif isinstance(obj, (list, tuple)):
        return type(obj)(force_obj_to_text(v, skip_unsupported) for v in obj)
    elif not skip_unsupported:
        raise ValueError("Unsupported type: {0}".format(type(obj)))
    else:
        return obj
