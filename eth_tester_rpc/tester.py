from eth_tester import (
    EthereumTester as _EthereumTester,
)
from eth_utils import (
    is_hex,
)

from .utils.validation import (
    validate_address,
)


class EthereumTester(_EthereumTester):

    def sign_message(self, address, message):
        validate_address(address)
        assert is_hex(message) is True, "message needs to be of type hex"
        return self.backend.sign_message(address, message)
