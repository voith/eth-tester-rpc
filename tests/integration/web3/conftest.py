from eth_utils import (
    to_bytes,
)
import pytest
from web3.utils.module_testing.emitter_contract import (
    EMITTER_ABI,
    EMITTER_BYTECODE,
)
from web3.utils.module_testing.math_contract import (
    MATH_ABI,
    MATH_BYTECODE,
)
from web3.utils.toolz import (
    identity,
)


@pytest.fixture(scope="module", params=[lambda x: to_bytes(hexstr=x), identity])
def address_conversion_func(request):
    return request.param


@pytest.fixture(scope="module")
def math_contract_factory(web3):
    contract_factory = web3.eth.contract(abi=MATH_ABI, bytecode=MATH_BYTECODE)
    return contract_factory


@pytest.fixture(scope="module")
def emitter_contract_factory(web3):
    contract_factory = web3.eth.contract(abi=EMITTER_ABI, bytecode=EMITTER_BYTECODE)
    return contract_factory
