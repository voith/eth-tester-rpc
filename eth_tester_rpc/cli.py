import random

import click

from .server import (
    get_application,
)
from .utils.compat_threading import (
    make_server,
    sleep,
    spawn,
)


@click.command()
@click.option(
    '--host',
    '-h',
    default='localhost',
)
@click.option(
    '--port',
    '-p',
    default=8545,
    type=int,
)
def runserver(host, port):
    application = get_application()

    print(application.rpc_methods.web3_clientVersion(None))

    print("\nListening on %s:%s" % (host, port))

    server = make_server(
        host,
        port,
        application,
    )

    spawn(server.serve_forever)

    try:
        while True:
            sleep(random.random())
    except KeyboardInterrupt:
        try:
            server.stop()
        except AttributeError:
            server.shutdown()


if __name__ == "__main__":
    runserver()
