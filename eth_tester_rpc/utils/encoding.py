"""
code copied from web3._utils.encoding
"""
# String encodings and numeric representations
from eth_utils import (
    add_0x_prefix,
    encode_hex,
    is_bytes,
    remove_0x_prefix,
    to_hex,
)

from .abi import (
    is_address_type,
    is_array_type,
    is_bool_type,
    is_bytes_type,
    is_int_type,
    is_string_type,
    is_uint_type,
    size_of_type,
    sub_type_of_array_type,
)
from .validation import (
    validate_abi_type,
    validate_abi_value,
)


def hex_encode_abi_type(abi_type, value, force_size=None):
    """
    Encodes value into a hex string in format of abi_type
    """
    validate_abi_type(abi_type)
    validate_abi_value(abi_type, value)

    data_size = force_size or size_of_type(abi_type)
    if is_array_type(abi_type):
        sub_type = sub_type_of_array_type(abi_type)
        return "".join([remove_0x_prefix(hex_encode_abi_type(sub_type, v, 256)) for v in value])
    elif is_bool_type(abi_type):
        return to_hex_with_size(value, data_size)
    elif is_uint_type(abi_type):
        return to_hex_with_size(value, data_size)
    elif is_int_type(abi_type):
        return to_hex_twos_compliment(value, data_size)
    elif is_address_type(abi_type):
        return pad_hex(value, data_size)
    elif is_bytes_type(abi_type):
        if is_bytes(value):
            return encode_hex(value)
        else:
            return value
    elif is_string_type(abi_type):
        return to_hex(text=value)
    else:
        raise ValueError(
            "Unsupported ABI type: {0}".format(abi_type)
        )


def to_hex_twos_compliment(value, bit_size):
    """
    Converts integer value to twos compliment hex representation with given bit_size
    """
    if value >= 0:
        return to_hex_with_size(value, bit_size)

    value = (1 << bit_size) + value
    hex_value = hex(value)
    hex_value = hex_value.rstrip("L")
    return hex_value


def to_hex_with_size(value, bit_size):
    """
    Converts a value to hex with given bit_size:
    """
    return pad_hex(to_hex(value), bit_size)


def pad_hex(value, bit_size):
    """
    Pads a hex string up to the given bit_size
    """
    value = remove_0x_prefix(value)
    return add_0x_prefix(value.zfill(int(bit_size / 4)))
