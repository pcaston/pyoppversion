"""Tests for Oppio."""
from unittest.mock import patch

import aiohttp
import pytest

from pyoppversion import OppVersion
from pyoppversion.consts import OppVersionChannel, OppVersionSource
from pyoppversion.exceptions import OppVersionInputException
from tests.common import fixture

from .const import HEADERS, STABLE_VERSION


@pytest.mark.asyncio
async def test_stable_version(aresponses):
    """Test oppio stable."""
    aresponses.add(
        "version.openpeerpower.io",
        "/stable.json",
        "get",
        aresponses.Response(
            text=fixture("supervised/default", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        oppversion = OppVersion(session=session, source=OppVersionSource.SUPERVISED)
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(OppVersion):
    """Test oppio beta."""
    with patch(
        "pyoppversion.supervised.OppVersionSupervised.data",
        fixture("supervised/default"),
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(
                session=session,
                source=OppVersionSource.SUPERVISED,
                channel=OppVersionChannel.BETA,
            )
            await oppversion.get_version()
            assert oppversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_input_exception(OppVersion):
    with pytest.raises(OppVersionInputException):
        OppVersion(source=OppVersionSource.SUPERVISED)
