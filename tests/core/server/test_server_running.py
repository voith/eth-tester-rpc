import os
import signal

from click.testing import (
    CliRunner,
)

from eth_tester_rpc.cli import (
    runserver,
)
from eth_tester_rpc.rpc import (
    RPCMethods,
)
from eth_tester_rpc.utils.compat_threading import (
    sleep,
    spawn,
)


def test_main_module_for_cli_server_running(open_port):
    runner = CliRunner()

    port = open_port

    pid = os.getpid()

    def kill_it():
        sleep(2)
        os.kill(pid, signal.SIGINT)

    spawn(kill_it)

    result = runner.invoke(runserver, ['--port', str(port)])
    assert result.exit_code == 0

    assert str(port) in result.output
    assert RPCMethods().web3_clientVersion([]) in result.output
