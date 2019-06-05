from eth_tester.backends.pyevm.main import (
    PyEVMBackend as _PyEVMBackend,
)
from eth_utils import (
    ValidationError,
    to_bytes,
)

from .utils.solidity import (
    solidityKeccak,
)


class PyEVMBackend(_PyEVMBackend):

    def sign_message(self, address, message):
        for key in self.account_keys:
            if key.public_key.to_checksum_address() == address:
                private_key = key
                break
        else:
            raise ValidationError(
                f'Could not find address: {address} in keychain.'
                f'Use personal_newAccount to add a new account with privateKey'
            )
        message_hash = to_bytes(hexstr=message)
        message_hash = solidityKeccak(
            ['string', 'bytes32'],
            ['\x19Ethereum Signed Message:\n32', message_hash]
        )
        return str(
            private_key.sign_msg_hash(message_hash)
        )
