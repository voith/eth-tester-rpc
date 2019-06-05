"""
code copied from web3._utils.validation
"""
from eth_utils import (
    is_0x_prefixed,
    is_binary_address,
    is_boolean,
    is_bytes,
    is_checksum_address,
    is_hex_address,
    is_integer,
    is_list_like,
    is_string,
)

from .abi import (
    is_address_type,
    is_array_type,
    is_bool_type,
    is_bytes_type,
    is_int_type,
    is_recognized_type,
    is_string_type,
    is_uint_type,
    length_of_array_type,
    sub_type_of_array_type,
)


class InvalidAddress(ValueError):
    """
    The supplied address does not have a valid checksum, as defined in EIP-55
    """
    pass


def validate_abi_type(abi_type):
    """
    Helper function for validating an abi_type
    """
    if not is_recognized_type(abi_type):
        raise ValueError("Unrecognized abi_type: {abi_type}".format(abi_type=abi_type))


def validate_abi_value(abi_type, value):
    """
    Helper function for validating a value against the expected abi_type
    Note: abi_type 'bytes' must either be python3 'bytes' object or ''
    """
    if is_array_type(abi_type) and is_list_like(value):
        # validate length
        specified_length = length_of_array_type(abi_type)
        if specified_length is not None:
            if specified_length < 1:
                raise TypeError(
                    "Invalid abi-type: {abi_type}. Length of fixed sized arrays"
                    "must be greater than 0."
                    .format(abi_type=abi_type)
                )
            if specified_length != len(value):
                raise TypeError(
                    "The following array length does not the length specified"
                    "by the abi-type, {abi_type}: {value}"
                    .format(abi_type=abi_type, value=value)
                )

        # validate sub_types
        sub_type = sub_type_of_array_type(abi_type)
        for v in value:
            validate_abi_value(sub_type, v)
        return
    elif is_bool_type(abi_type) and is_boolean(value):
        return
    elif is_uint_type(abi_type) and is_integer(value) and value >= 0:
        return
    elif is_int_type(abi_type) and is_integer(value):
        return
    elif is_address_type(abi_type):
        validate_address(value)
        return
    elif is_bytes_type(abi_type):
        if is_bytes(value):
            return
        elif is_string(value):
            if is_0x_prefixed(value):
                return
            else:
                raise TypeError(
                    "ABI values of abi-type 'bytes' must be either"
                    "a python3 'bytes' object or an '0x' prefixed string."
                )
    elif is_string_type(abi_type) and is_string(value):
        return

    raise TypeError(
        "The following abi value is not a '{abi_type}': {value}"
        .format(abi_type=abi_type, value=value)
    )


def validate_address(value):
    """
    Helper function for validating an address
    """
    if is_bytes(value):
        if not is_binary_address(value):
            raise InvalidAddress("Address must be 20 bytes when input type is bytes", value)
        return

    if not isinstance(value, str):
        raise TypeError('Address {} must be provided as a string'.format(value))
    if not is_hex_address(value):
        raise InvalidAddress("Address must be 20 bytes, as a hex string with a 0x prefix", value)
    if not is_checksum_address(value):
        if value == value.lower():
            raise InvalidAddress(
                "Web3.py only accepts checksum addresses. "
                "The software that gave you this non-checksum address should be considered unsafe, "
                "please file it as a bug on their platform. "
                "Try using an ENS name instead. Or, if you must accept lower safety, "
                "use Web3.toChecksumAddress(lower_case_address).",
                value,
            )
        else:
            raise InvalidAddress(
                "Address has an invalid EIP-55 checksum. "
                "After looking up the address from the original source, try again.",
                value,
            )
