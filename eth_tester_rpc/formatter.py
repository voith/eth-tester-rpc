import operator

from eth_utils import (
    is_dict,
    is_hex,
    is_string,
)

from eth_tester_rpc.utils.formatters import (
    apply_formatter_if,
    apply_formatter_to_array,
    apply_formatters_to_args,
    apply_formatters_to_dict,
    apply_key_map,
    hex_to_integer,
    integer_to_hex,
    is_array_of_dicts,
    remove_key_if,
    static_return,
)
from eth_tester_rpc.utils.toolz import (
    assoc,
    complement,
    compose,
    curry,
    identity,
    partial,
    pipe,
)


def is_named_block(value):
    return value in {"latest", "earliest", "pending"}


def is_hexstr(value):
    return is_string(value) and is_hex(value)


to_integer_if_hex = apply_formatter_if(is_hexstr, hex_to_integer)


is_not_named_block = complement(is_named_block)


TRANSACTION_KEY_MAPPINGS = {
    'block_hash': 'blockHash',
    'block_number': 'blockNumber',
    'gas_price': 'gasPrice',
    'transaction_hash': 'transactionHash',
    'transaction_index': 'transactionIndex',
}

transaction_key_remapper = apply_key_map(TRANSACTION_KEY_MAPPINGS)


LOG_KEY_MAPPINGS = {
    'log_index': 'logIndex',
    'transaction_index': 'transactionIndex',
    'transaction_hash': 'transactionHash',
    'block_hash': 'blockHash',
    'block_number': 'blockNumber',
}


log_key_remapper = apply_key_map(LOG_KEY_MAPPINGS)


RECEIPT_KEY_MAPPINGS = {
    'block_hash': 'blockHash',
    'block_number': 'blockNumber',
    'contract_address': 'contractAddress',
    'gas_used': 'gasUsed',
    'cumulative_gas_used': 'cumulativeGasUsed',
    'transaction_hash': 'transactionHash',
    'transaction_index': 'transactionIndex',
}


receipt_key_remapper = apply_key_map(RECEIPT_KEY_MAPPINGS)


BLOCK_KEY_MAPPINGS = {
    'gas_limit': 'gasLimit',
    'sha3_uncles': 'sha3Uncles',
    'transactions_root': 'transactionsRoot',
    'parent_hash': 'parentHash',
    'bloom': 'logsBloom',
    'state_root': 'stateRoot',
    'receipt_root': 'receiptsRoot',
    'total_difficulty': 'totalDifficulty',
    'extra_data': 'extraData',
    'gas_used': 'gasUsed',
}


# This is needed when transactions are returned as a part of requested block in their full form (not just ids),
# such as when calling web3.eth.getBlock(123, fullTransactions=True)
BLOCK_NESTED_REMAPPERS = {
    'transactions': apply_formatter_to_array(apply_formatter_if(is_dict, transaction_key_remapper)),
}


block_key_remapper = compose(
    apply_formatters_to_dict(BLOCK_NESTED_REMAPPERS),
    apply_key_map(BLOCK_KEY_MAPPINGS),
)


TRANSACTION_PARAMS_MAPPING = {
    'gasPrice': 'gas_price',
}


transaction_params_remapper = apply_key_map(TRANSACTION_PARAMS_MAPPING)


TRANSACTION_PARAMS_FORMATTERS = {
    'gas': to_integer_if_hex,
    'gasPrice': to_integer_if_hex,
    'value': to_integer_if_hex,
    'nonce': to_integer_if_hex,
}


transaction_params_formatter = compose(
    # remove nonce for now due to issue https://github.com/ethereum/eth-tester/issues/80
    remove_key_if('nonce', lambda _: True),
    apply_formatters_to_dict(TRANSACTION_PARAMS_FORMATTERS),
)


FILTER_PARAMS_MAPPINGS = {
    'fromBlock': 'from_block',
    'toBlock': 'to_block',
}

filter_params_remapper = apply_key_map(FILTER_PARAMS_MAPPINGS)

FILTER_PARAMS_FORMATTERS = {
    'fromBlock': to_integer_if_hex,
    'toBlock': to_integer_if_hex,
}

filter_params_formatter = apply_formatters_to_dict(FILTER_PARAMS_FORMATTERS)

filter_params_transformer = compose(
    remove_key_if('address', lambda x: not x['address']),
    filter_params_remapper,
    filter_params_formatter
)


TRANSACTION_FORMATTERS = {
    'to': apply_formatter_if(partial(operator.eq, ''), static_return(None)),
}


transaction_formatter = apply_formatters_to_dict(TRANSACTION_FORMATTERS)


RECEIPT_FORMATTERS = {
    'logs': apply_formatter_to_array(log_key_remapper),
}


receipt_formatter = apply_formatters_to_dict(RECEIPT_FORMATTERS)

transaction_params_transformer = compose(transaction_params_remapper, transaction_params_formatter)


default_request_formatters = {
    # Eth
    'eth_getBlockByNumber': apply_formatters_to_args(
        apply_formatter_if(is_not_named_block, to_integer_if_hex),
    ),
    'eth_getFilterChanges': apply_formatters_to_args(hex_to_integer),
    'eth_getFilterLogs': apply_formatters_to_args(hex_to_integer),
    'eth_getBlockTransactionCountByNumber': apply_formatters_to_args(
        apply_formatter_if(is_not_named_block, to_integer_if_hex),
    ),
    'eth_getUncleCountByBlockNumber': apply_formatters_to_args(
        apply_formatter_if(is_not_named_block, to_integer_if_hex),
    ),
    'eth_getTransactionByBlockHashAndIndex': apply_formatters_to_args(
        identity,
        to_integer_if_hex,
    ),
    'eth_getTransactionByBlockNumberAndIndex': apply_formatters_to_args(
        apply_formatter_if(is_not_named_block, to_integer_if_hex),
        to_integer_if_hex,
    ),
    'eth_getUncleByBlockNumberAndIndex': apply_formatters_to_args(
        apply_formatter_if(is_not_named_block, to_integer_if_hex),
        to_integer_if_hex,
    ),
    'eth_newFilter': apply_formatters_to_args(
        filter_params_transformer,
    ),
    'eth_getLogs': apply_formatters_to_args(
        filter_params_transformer,
    ),
    'eth_sendTransaction': apply_formatters_to_args(
        transaction_params_transformer,
    ),
    'eth_estimateGas': apply_formatters_to_args(
        transaction_params_transformer,
    ),
    'eth_call': apply_formatters_to_args(
        transaction_params_transformer,
        apply_formatter_if(is_not_named_block, to_integer_if_hex),
    ),
    'eth_uninstallFilter': apply_formatters_to_args(hex_to_integer),
    'eth_getCode': apply_formatters_to_args(
        identity,
        apply_formatter_if(is_not_named_block, to_integer_if_hex),
    ),
    # EVM
    'evm_revert': apply_formatters_to_args(hex_to_integer),
    # Personal
    'personal_sendTransaction': apply_formatters_to_args(
        transaction_params_transformer,
        identity,
    ),
}

default_result_formatters = {
    'eth_getBlockByHash': apply_formatter_if(
        is_dict,
        block_key_remapper,
    ),
    'eth_getBlockByNumber': apply_formatter_if(
        is_dict,
        block_key_remapper,
    ),
    'eth_getBlockTransactionCountByHash': apply_formatter_if(
        is_dict,
        transaction_key_remapper,
    ),
    'eth_getBlockTransactionCountByNumber': apply_formatter_if(
        is_dict,
        transaction_key_remapper,
    ),
    'eth_getTransactionByHash': apply_formatter_if(
        is_dict,
        compose(transaction_key_remapper, transaction_formatter),
    ),
    'eth_getTransactionReceipt': apply_formatter_if(
        is_dict,
        compose(receipt_key_remapper, receipt_formatter),
    ),
    'eth_newFilter': integer_to_hex,
    'eth_newBlockFilter': integer_to_hex,
    'eth_newPendingTransactionFilter': integer_to_hex,
    'eth_getLogs': apply_formatter_if(
        is_array_of_dicts,
        apply_formatter_to_array(log_key_remapper),
    ),
    'eth_getFilterChanges': apply_formatter_if(
        is_array_of_dicts,
        apply_formatter_to_array(log_key_remapper),
    ),
    'eth_getFilterLogs': apply_formatter_if(
        is_array_of_dicts,
        apply_formatter_to_array(log_key_remapper),
    ),
    # EVM
    'evm_snapshot': integer_to_hex,
}


@curry
def apply_dict_formatter(method, data, formatters):
    if method in formatters:
        formatter = formatters[method]
        return formatter(data)
    else:
        return data


def request_formatter(method, params):
    return apply_dict_formatter(
        method=method,
        data=params,
        formatters=default_request_formatters
    )


def result_formatter(method, result):
    return apply_dict_formatter(
        method=method,
        data=result,
        formatters=default_result_formatters
    )


ethereum_tester_fixture = {
    # Eth
    'eth_protocolVersion': '63',
    'eth_hashrate': 0,
    'eth_gasPrice': 1,
    'eth_syncing': False,
    'eth_mining': False,
    # Net
    'net_version': '1',
    'net_listening': False,
    'net_peerCount': 0,
}


def guess_from(client, transaction):
    try:
        return client.get_accounts()[0]
    except KeyError as e:
        # no accounts available to pre-fill, carry on
        pass

    return None


def guess_gas(client, transaction):
    return client.estimate_gas(transaction) * 2


@curry
def fill_default(field, guess_func, client, transaction):
    if field in transaction and transaction[field] is not None:
        return transaction
    else:
        guess_val = guess_func(client, transaction)
        return assoc(transaction, field, guess_val)


def default_value_formatter(client):
    fill_default_from = fill_default('from', guess_from, client)
    fill_default_gas = fill_default('gas', guess_gas, client)

    def call_formatter(method, params):
        if method in (
                'eth_call',
                'eth_estimateGas',
                'eth_sendTransaction',
        ):
            filled_transaction = pipe(
                params[0],
                fill_default_from,
                fill_default_gas,
            )
            return (filled_transaction,) + params[1:]
        else:
            return params
    return call_formatter


def _apply_formatter(method, data, formatters):
    for formatter in formatters:
        data = formatter(method, data)
    return data


class Formatter:

    def __init__(self, request_formatters, result_formatters):
        self.request_formatters = request_formatters
        self.result_formatters = result_formatters

    def apply_request_formatter(self, method, params):
        return _apply_formatter(
            method,
            params,
            self.request_formatters
        )

    def apply_result_formatter(self, method, result):
        return _apply_formatter(
            method,
            result,
            self.result_formatters
        )
