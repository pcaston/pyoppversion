import logging
from unittest.mock import patch

import pytest

from pyopversion import OpVersion as PyOpVersion

logging.basicConfig(level=logging.DEBUG)
pytestmark = pytest.mark.asyncio


async def mocked_fetch(self):
    pass


@pytest.fixture
def OpVersion():
    with patch(
        "pyopversion.container.OpVersionContainer.fetch", return_value=mocked_fetch
    ), patch("pyopversion.opio.OpVersionOpio.fetch", return_value=mocked_fetch), patch(
        "pyopversion.local.OpVersionLocal.fetch", return_value=mocked_fetch
    ), patch(
        "pyopversion.pypi.OpVersionPypi.fetch", return_value=mocked_fetch
    ), patch(
        "pyopversion.supervisor.OpVersionSupervisor.fetch", return_value=mocked_fetch
    ):
        yield PyOpVersion
