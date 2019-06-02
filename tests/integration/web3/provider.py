from wsgiref.simple_server import (
    make_server,
)

from web3.providers import (
    HTTPProvider,
)
from web3.middleware import (
    construct_fixture_middleware,
)
from .threads import (
    spawn,
)

from eth_tester_rpc.server import (
    get_application,
)

ethereum_tester_fixture_middleware = construct_fixture_middleware({
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
})


class EthTestRPCProvider(HTTPProvider):
    middlewares = [
        ethereum_tester_fixture_middleware,
    ]

    def __init__(self, host="127.0.0.1", port=8545, *args, **kwargs):

        self.application = get_application()

        self.server = make_server(
            host,
            port,
            self.application,
        )

        self.thread = spawn(self.server.serve_forever)
        endpoint_uri = 'http://{0}:{1}'.format(host, port)

        super().__init__(endpoint_uri, *args, **kwargs)
