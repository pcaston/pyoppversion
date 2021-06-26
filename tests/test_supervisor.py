"""Tests for Hassio."""
from unittest.mock import patch

import aiohttp
import pytest

from pyopversion import OpVersion
from pyopversion.consts import OpVersionChannel, OpVersionSource
from pyopversion.exceptions import OpVersionInputException
from tests.common import fixture

from .const import HEADERS, STABLE_VERSION


@pytest.mark.asyncio
async def test_stable_version(aresponses):
    """Test hassio stable."""
    aresponses.add(
        "version.open-peer-power.io",
        "/stable.json",
        "get",
        aresponses.Response(
            text=fixture("supervisor/default", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        opversion = OpVersion(session=session, source=OpVersionSource.SUPERVISOR)
        await opversion.get_version()
        assert opversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(OpVersion):
    """Test hassio beta."""
    with patch(
        "pyopversion.supervisor.OpVersionSupervisor.data",
        fixture("supervisor/default"),
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(
                session=session,
                source=OpVersionSource.SUPERVISOR,
                channel=OpVersionChannel.BETA,
                board="test",
                image="test",
            )
            await opversion.get_version()
            assert opversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_input_exception(OpVersion):
    with pytest.raises(OpVersionInputException):
        OpVersion(source=OpVersionSource.SUPERVISOR)
