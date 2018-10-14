from wsgiref.simple_server import (
    make_server,
)

from web3.providers import (
    HTTPProvider,
)
from web3.providers.eth_tester.middleware import (
    ethereum_tester_fixture_middleware,
)
from web3.utils.threads import (
    spawn,
)

from eth_tester_rpc.server import (
    get_application,
)


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
