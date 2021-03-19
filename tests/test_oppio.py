"""Tests for opp.io/version.json."""
import aiohttp
import pytest

from pyoppversion import OppVersion
from pyoppversion.consts import OppVersionSource
from pyoppversion.exceptions import OppVersionInputException
from tests.common import fixture

from .const import HEADERS, STABLE_VERSION


@pytest.mark.asyncio
async def test_oppio(aresponses):
    """Test opp.io/version.json stable."""
    aresponses.add(
        "www.openpeerpower.io",
        "/version.json",
        "get",
        aresponses.Response(
            text=fixture("oppio/default", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        oppversion = OppVersion(session=session, source=OppVersionSource.OPPIO)
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_input_exception(OppVersion):
    with pytest.raises(OppVersionInputException):
        OppVersion(source=OppVersionSource.OPPIO)
