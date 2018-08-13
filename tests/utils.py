
from eth_tester_rpc.utils.compat_threading import (  # noqa: E402
    Timeout,
    sleep,
    socket,
)


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return int(port)


def wait_for_http_connection(port, timeout=5):
    with Timeout(timeout) as _timeout:
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                s.connect(('127.0.0.1', port))
            except (socket.timeout, ConnectionRefusedError):
                sleep(0.1)
                _timeout.check()
                continue
            else:
                s.close()
                break
        else:
            raise ValueError("Unable to establish HTTP connection")
