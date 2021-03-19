"""Tests for PyPi."""
from unittest.mock import patch

import aiohttp
import pytest

from pyoppversion import OppVersion
from pyoppversion.consts import OppVersionChannel, OppVersionSource
from pyoppversion.exceptions import OppVersionInputException
from tests.common import fixture

from .const import BETA_VERSION, HEADERS, STABLE_VERSION, STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_stable_version(OppVersion):
    """Test pypi stable."""
    with patch(
        "pyoppversion.pypi.OppVersionPypi.data",
        fixture("pypi/default"),
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(
                session=session,
                source=OppVersionSource.PYPI,
            )
            await oppversion.get_version()
            assert oppversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(OppVersion):
    """Test pypi beta."""
    with patch(
        "pyoppversion.pypi.OppVersionPypi.data",
        fixture("pypi/beta"),
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(
                session=session,
                source=OppVersionSource.PYPI,
                channel=OppVersionChannel.BETA,
            )
            await oppversion.get_version()
            assert oppversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(aresponses):
    """Test pypi stable during beta week."""
    aresponses.add(
        "pypi.org",
        "/pypi/openpeerpower/json",
        "get",
        aresponses.Response(
            text=fixture("pypi/beta", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        oppversion = OppVersion(
            session=session,
            source=OppVersionSource.PYPI,
        )
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_input_exception(OppVersion):
    with pytest.raises(OppVersionInputException):
        OppVersion(source=OppVersionSource.PYPI)
