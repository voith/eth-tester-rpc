from eth_abi import (
    encode_abi,
)
from eth_utils import (
    encode_hex,
)


def test_eth_filter(
    rpc_client,
    client_call_emitter,
    Events,
    LogFunctions,
    LogTopics
):
    filter_id = rpc_client('eth_newFilter', params=[{
        "fromBlock": "latest",
        "toBlock": "latest",
    }])

    client_call_emitter(
        LogFunctions.logSingle,
        [Events.LogSingleWithIndex, 1234567890],
    )

    changes = rpc_client('eth_getFilterLogs', params=[filter_id])

    assert len(changes) == 1
    log_entry = changes[0]

    assert LogTopics.LogSingleWithIndex in log_entry['topics']
    assert encode_hex(encode_abi(['int'], [1234567890])) in log_entry['topics']
