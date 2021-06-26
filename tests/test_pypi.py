"""Tests for PyPi."""
from unittest.mock import patch

import aiohttp
import pytest

from pyopversion import OpVersion
from pyopversion.consts import OpVersionChannel, OpVersionSource
from pyopversion.exceptions import OpVersionInputException
from tests.common import fixture

from .const import BETA_VERSION, HEADERS, STABLE_VERSION, STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_stable_version(OpVersion):
    """Test pypi stable."""
    with patch(
        "pyopversion.pypi.OpVersionPypi.data",
        fixture("pypi/default"),
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(
                session=session,
                source=OpVersionSource.PYPI,
            )
            await opversion.get_version()
            assert opversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(OpVersion):
    """Test pypi beta."""
    with patch(
        "pyopversion.pypi.OpVersionPypi.data",
        fixture("pypi/beta"),
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(
                session=session,
                source=OpVersionSource.PYPI,
                channel=OpVersionChannel.BETA,
            )
            await opversion.get_version()
            assert opversion.version == BETA_VERSION


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
        opversion = OpVersion(
            session=session,
            source=OpVersionSource.PYPI,
        )
        await opversion.get_version()
        assert opversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_input_exception(OpVersion):
    with pytest.raises(OpVersionInputException):
        OpVersion(source=OpVersionSource.PYPI)
