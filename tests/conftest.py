import logging
from unittest.mock import patch

import pytest

from pyoppversion import OppVersion as PyOppVersion

logging.basicConfig(level=logging.DEBUG)
pytestmark = pytest.mark.asyncio


async def mocked_fetch(self):
    pass


@pytest.fixture
def OppVersion():
    with patch(
        "pyoppversion.docker.OppVersionDocker.fetch", return_value=mocked_fetch
    ), patch("pyoppversion.oppio.OppVersionOPPIO.fetch", return_value=mocked_fetch), patch(
        "pyoppversion.local.OppVersionLocal.fetch", return_value=mocked_fetch
    ), patch(
        "pyoppversion.pypi.OppVersionPypi.fetch", return_value=mocked_fetch
    ), patch(
        "pyoppversion.supervised.OppVersionSupervised.fetch", return_value=mocked_fetch
    ):
        yield PyOppVersion
