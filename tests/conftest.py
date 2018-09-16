import pytest

from tests.utils import (
    get_open_port,
)


@pytest.fixture()
def open_port():
    return get_open_port()
