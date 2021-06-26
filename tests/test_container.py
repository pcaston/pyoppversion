"""Tests for Container."""

import json
from unittest.mock import patch

import aiohttp
import pytest

from pyopversion import OpVersion
from pyopversion.consts import OpVersionChannel, OpVersionSource
from pyopversion.exceptions import OpVersionInputException
from tests.common import fixture

from .const import (
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
    DEV_VERSION,
    HEADERS,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
)


@pytest.mark.asyncio
async def test_stable_version(OpVersion):
    """Test container stable."""
    with patch(
        "pyopversion.container.OpVersionContainer.data",
        fixture("container/default"),
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(session=session, source=OpVersionSource.CONTAINER)
            await opversion.get_version()
            assert opversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(OpVersion):
    """Test container beta."""
    with patch(
        "pyopversion.container.OpVersionContainer.data",
        fixture("container/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(
                session=session,
                source=OpVersionSource.CONTAINER,
                channel=OpVersionChannel.BETA,
            )
            await opversion.get_version()
            assert opversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_dev_version(OpVersion):
    """Test container dev."""
    with patch(
        "pyopversion.container.OpVersionContainer.data",
        fixture("container/default"),
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(
                session=session,
                source=OpVersionSource.CONTAINER,
                channel=OpVersionChannel.DEV,
            )
            await opversion.get_version()
            assert opversion.version == DEV_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(OpVersion):
    """Test container stable during beta week."""
    with patch(
        "pyopversion.container.OpVersionContainer.data",
        fixture("container/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(
                session=session,
                source=OpVersionSource.CONTAINER,
            )
            await opversion.get_version()
            assert opversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(OpVersion):
    """Test container beta during beta week."""
    with patch(
        "pyopversion.container.OpVersionContainer.data",
        fixture("container/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(
                session=session,
                source=OpVersionSource.CONTAINER,
                channel=OpVersionChannel.BETA,
            )
        await opversion.get_version()
        assert opversion.version == BETA_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_stable_version_pagination(aresponses):
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/open-peer-power/tags",
        "get",
        aresponses.Response(
            text=fixture("container/page1", False), status=200, headers=HEADERS
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/open-peer-power/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/page2", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        opversion = OpVersion(
            session=session,
            source=OpVersionSource.CONTAINER,
        )
        await opversion.get_version()
        assert opversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version_pagination(aresponses):
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/open-peer-power/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/open-peer-power/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )
    async with aiohttp.ClientSession() as session:
        opversion = OpVersion(
            session=session,
            source=OpVersionSource.CONTAINER,
            channel=OpVersionChannel.BETA,
        )
        await opversion.get_version()
        assert opversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week_pagination(aresponses):
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/open-peer-power/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/open-peer-power/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        opversion = OpVersion(
            session=session,
            source=OpVersionSource.CONTAINER,
        )
        await opversion.get_version()
        assert opversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week_pagination(aresponses):
    """Test container beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/open-peer-power/tags",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/open-peer-power/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("container/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        opversion = OpVersion(
            session=session,
            source=OpVersionSource.CONTAINER,
            channel=OpVersionChannel.BETA,
        )
        await opversion.get_version()
        assert opversion.version == BETA_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_input_exception(OpVersion):
    with pytest.raises(OpVersionInputException):
        OpVersion(source=OpVersionSource.CONTAINER)
