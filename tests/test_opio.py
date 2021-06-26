"""Tests for op.io/version.json."""
import aiohttp
import pytest

from pyopversion import OpVersion
from pyopversion.consts import OpVersionSource
from pyopversion.exceptions import OpVersionInputException
from tests.common import fixture

from .const import HEADERS, STABLE_VERSION


@pytest.mark.asyncio
async def test_opio(aresponses):
    """Test ha.io/version.json stable."""
    aresponses.add(
        "version.openpeerpower.io/",
        "/stable.json",
        "get",
        aresponses.Response(
            text=fixture("opio/default", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        opversion = OpVersion(session=session, source=OpVersionSource.OPIO)
        await opversion.get_version()
        assert opversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_input_exception(OpVersion):
    with pytest.raises(OpVersionInputException):
        OpVersion(source=OpVersionSource.OPIO)
