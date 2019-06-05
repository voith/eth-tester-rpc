from eth_utils import (
    add_0x_prefix,
    apply_to_return_value,
    keccak as eth_utils_keccak,
    remove_0x_prefix,
    to_bytes,
)
from eth_utils.toolz import (
    curry,
)
from hexbytes import (
    HexBytes,
)

from .abi import (
    map_abi_data,
)
from .encoding import (
    hex_encode_abi_type,
)


@curry
def abi_ens_resolver(type_str, val):
    return type_str, val


@apply_to_return_value(HexBytes)
def keccak(primitive=None, text=None, hexstr=None):
    if isinstance(primitive, (bytes, int, type(None))):
        input_bytes = to_bytes(primitive, hexstr=hexstr, text=text)
        return eth_utils_keccak(input_bytes)

    raise TypeError(
        "You called keccak with first arg %r and keywords %r. You must call it with one of "
        "these approaches: keccak(text='txt'), keccak(hexstr='0x747874'), "
        "keccak(b'\\x74\\x78\\x74'), or keccak(0x747874)." % (
            primitive,
            {'text': text, 'hexstr': hexstr}
        )
    )


def solidityKeccak(abi_types, values):
    """
    Executes keccak256 exactly as Solidity does.
    Takes list of abi_types as inputs -- `[uint24, int8[], bool]`
    and list of corresponding values  -- `[20, [-1, 5, 0], True]`
    """
    if len(abi_types) != len(values):
        raise ValueError(
            "Length mismatch between provided abi types and values.  Got "
            "{0} types and {1} values.".format(len(abi_types), len(values))
        )

    normalized_values = map_abi_data([abi_ens_resolver], abi_types, values)

    hex_string = add_0x_prefix(''.join(
        remove_0x_prefix(hex_encode_abi_type(abi_type, value))
        for abi_type, value
        in zip(abi_types, normalized_values)
    ))
    return keccak(hexstr=hex_string)
