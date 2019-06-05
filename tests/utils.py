from eth_abi import (
    encode_abi,
)
from eth_keys.datatypes import (
    Signature,
)
from eth_utils import (
    encode_hex,
    keccak,
    to_bytes,
    to_hex,
)

from eth_tester_rpc.utils.compat_threading import (  # noqa: E402
    Timeout,
    sleep,
    socket,
)
from eth_tester_rpc.utils.solidity import (
    solidityKeccak,
)


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return int(port)


def wait_for_http_connection(port, timeout=5):
    with Timeout(timeout) as _timeout:
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                s.connect(('127.0.0.1', port))
            except (socket.timeout, ConnectionRefusedError):
                sleep(0.1)
                _timeout.check()
                continue
            else:
                s.close()
                break
        else:
            raise ValueError("Unable to establish HTTP connection")


def function_to_4_byte_selector(method_signature):
    return encode_hex(keccak(text=method_signature)[:4])


def get_abi_input_types(abi):
    if 'inputs' not in abi and abi['type'] == 'fallback':
        return []
    else:
        return [arg['type'] for arg in abi['inputs']]


def _abi_to_signature(abi):
    function_signature = "{fn_name}({fn_input_types})".format(
        fn_name=abi['name'],
        fn_input_types=','.join([
            arg['type'] for arg in abi.get('inputs', [])
        ]),
    )
    return function_signature


def get_function_abi(contract_abi, method_signature):
    """
    Assumes that contract has only method with same name
    """
    for abi in contract_abi:
        if _abi_to_signature(abi) == method_signature:
            return abi
    else:
        raise ValueError


def encode_fn_abi(abi, method_signature, arguments):
    fn_abi = get_function_abi(abi, method_signature)
    function_sig = keccak(text=method_signature)[:4]
    return to_hex(
        function_sig + encode_abi(get_abi_input_types(fn_abi), arguments)
    )


def close_http_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(('127.0.0.1', port))
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        pass


def hex_to_int(val):
    return int(val, 16)


def ecrecover(signature, message):
    message_hash = to_bytes(hexstr=message)
    message_hash = solidityKeccak(
        ['string', 'bytes32'],
        ['\x19Ethereum Signed Message:\n32', message_hash]
    )
    _signature = Signature(to_bytes(hexstr=signature))
    public_key = _signature.recover_public_key_from_msg_hash(message_hash)
    return public_key.to_checksum_address()
