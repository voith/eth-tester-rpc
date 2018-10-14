

def test_eth_getLogs(
    rpc_client,
    client_call_emitter,
    Events,
    LogFunctions,
    LogTopics
):
    client_call_emitter(LogFunctions.logNoArgs, [Events.LogNoArguments])
    filter_params = {
        "fromBlock": 0,
        "toBlock": "latest",
    }
    result = rpc_client('eth_getLogs', params=[filter_params])
    assert len(result) == 1
    log_entry = result[0]
    assert LogTopics.LogNoArguments in log_entry['topics']
