from eth_abi import (
    encode_abi,
)
from eth_utils import (
    encode_hex,
)
import pytest


def test_new_filter_no_events(rpc_client):
    filter_id = rpc_client('eth_newFilter', params=[{
        "fromBlock": "latest",
        "toBlock": "latest",
        "address": [],
        "topics": []
    }])

    changes = rpc_client('eth_getFilterLogs', params=[filter_id])

    assert changes == []


def test_new_filter_with_single_no_args_event(
        rpc_client,
        client_call_emitter,
        Events,
        LogFunctions,
        LogTopics
):
    filter_id = rpc_client('eth_newFilter', params=[{
        "fromBlock": "latest",
        "toBlock": "latest",
        "address": [],
        "topics": []
    }])

    client_call_emitter(LogFunctions.logNoArgs, [Events.LogNoArguments])

    changes = rpc_client('eth_getFilterLogs', params=[filter_id])

    assert len(changes) == 1
    log_entry = changes[0]
    assert LogTopics.LogNoArguments in log_entry['topics']


def test_new_filter_block_numbers_hex(
        rpc_client,
        client_call_emitter,
        Events,
        LogFunctions,
        LogTopics
):
    filter_id = rpc_client('eth_newFilter', params=[{
        "fromBlock": "0x0",
        "toBlock": "0x2",
        # "address": [],
        "topics": []
    }])

    client_call_emitter(LogFunctions.logNoArgs, [Events.LogNoArguments])

    changes = rpc_client('eth_getFilterLogs', params=[filter_id])

    assert len(changes) == 1
    log_entry = changes[0]
    assert LogTopics.LogNoArguments in log_entry['topics']


def test_new_filter_with_anonymous_event(
        rpc_client,
        client_call_emitter,
        LogFunctions,
        Events
):
    filter_id = rpc_client('eth_newFilter', params=[{
        "fromBlock": "latest",
        "toBlock": "latest",
        "address": [],
        "topics": []
    }])

    client_call_emitter(LogFunctions.logNoArgs, [Events.LogAnonymous])

    changes = rpc_client('eth_getFilterLogs', params=[filter_id])

    assert len(changes) == 1
    log_entry = changes[0]
    assert not log_entry['topics']  # anonymous event


@pytest.mark.xfail
def test_new_filter_with_topic_based_filtering(
        rpc_client,
        client_call_emitter,
        LogFunctions,
        LogTopics,
        Events
):
    filter_id = rpc_client('eth_newFilter', params=[{
        "fromBlock": "earliest",
        "toBlock": "latest",
        "address": [],
        "topics": [[LogTopics.LogSingleArg], [LogTopics.LogNoArguments]]
    }])

    client_call_emitter(LogFunctions.logDouble, [Events.LogDoubleWithIndex, 1234, 4321])
    client_call_emitter(LogFunctions.logNoArgs, [Events.LogNoArguments])
    client_call_emitter(LogFunctions.logSingle, [Events.LogSingleArg, 1234])
    client_call_emitter(LogFunctions.logDouble, [Events.LogDoubleWithIndex, 5678, 8765])

    changes = rpc_client('eth_getFilterLogs', params=[filter_id])

    assert len(changes) == 2
    log_entry_a, log_entry_b = changes

    assert LogTopics.LogNoArguments in log_entry_a['topics']
    assert LogTopics.LogSingleArg in log_entry_b['topics']


def test_new_filter_with_topic_filter_on_indexed_arg(
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
