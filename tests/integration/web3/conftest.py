from eth_utils import (
    to_bytes,
)
from eth_utils.toolz import (
    identity,
)
import pytest
from web3._utils.module_testing.emitter_contract import (
    CONTRACT_EMITTER_ABI,
    CONTRACT_EMITTER_CODE,
)
from web3._utils.module_testing.math_contract import (
    MATH_ABI,
    MATH_BYTECODE,
)
from web3._utils.module_testing.revert_contract import (
    _REVERT_CONTRACT_ABI,
    REVERT_CONTRACT_BYTECODE,
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
    contract_factory = web3.eth.contract(abi=CONTRACT_EMITTER_ABI, bytecode=CONTRACT_EMITTER_CODE)
    return contract_factory


@pytest.fixture(scope="module")
def revert_contract_factory(web3):
    contract_factory = web3.eth.contract(
        abi=_REVERT_CONTRACT_ABI,
        bytecode=REVERT_CONTRACT_BYTECODE
    )
    return contract_factory
