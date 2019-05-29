# eth-tester-rpc

[![Join the chat at https://gitter.im/eth-tester-rpc/Lobby](https://badges.gitter.im/eth-tester-rpc/Lobby.svg)](https://gitter.im/eth-tester-rpc/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://circleci.com/gh/voith/eth-tester-rpc.svg?style=shield)](https://circleci.com/gh/voith/eth-tester-rpc)
[![PyPI version](https://badge.fury.io/py/eth-tester-rpc.svg)](https://badge.fury.io/py/eth-tester-rpc)
[![Python versions](https://img.shields.io/pypi/pyversions/eth-tester-rpc.svg)](https://pypi.python.org/pypi/eth-tester-rpc) 
   

A rewrite of [Piper Merriam's eth-testrpc](https://github.com/pipermerriam/eth-testrpc/tree/master/testrpc) using [eth-tester](https://github.com/ethereum/eth-tester)

The `eth-teste-rpc` is a tool for testing any code that needs to make calls to ethereums RPC API. It starts a server to which you can connect your application and run tests accordingly.It is built on top of [py-evm](https://github.com/ethereum/py-evm).

## Quickstart

```sh
pip install eth-tester-rpc
```

To check usage of the command:
```bash
$ py-testrpc --help

Options:
  -h, --host TEXT
  -p, --port INTEGER
  --help              Show this message and exit.
```

To start the server:
```bash
py-testrpc -p 8888
```
The above command will start a server at port 8888. The default port is 8545.

To make a connection using web3.py
```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8888"))
print(w3.eth.blockNumber)
```

## Developer Setup

If you would like to hack on eth-tester-rpc, please check out the
[Ethereum Development Tactical Manual](https://github.com/pipermerriam/ethereum-dev-tactical-manual)
for information on how we do:

- Testing
- Pull Requests
- Code Style
- Documentation

### Development Environment Setup

You can set up your dev environment with:

```sh
git clone git@github.com:voith/eth-tester-rpc.git
cd eth-tester-rpc
virtualenv -p python3 venv
. venv/bin/activate
pip install -e .[dev]
```

### Testing Setup

During development, you might like to have tests run on every file save.

Show flake8 errors on file change:

```sh
# Test flake8
when-changed -v -s -r -1 eth_tester_rpc/ tests/ -c "clear; flake8 eth_tester_rpc tests && echo 'flake8 success' || echo 'error'"
```

Run multi-process tests in one command, but without color:

```sh
# in the project root:
pytest --numprocesses=4 --looponfail --maxfail=1
# the same thing, succinctly:
pytest -n 4 -f --maxfail=1
```

Run in one thread, with color and desktop notifications:

```sh
cd venv
ptw --onfail "notify-send -t 5000 'Test failure ⚠⚠⚠⚠⚠' 'python 3 test on eth_tester_rpc failed'" ../tests ../eth_tester_rpc
```

### Release setup

For Debian-like systems:
```
apt install pandoc
```

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```

#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`.

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 4.0.0-alpha.1 devnum"`
