"""Tests for Docker."""

import json
from unittest.mock import patch

import aiohttp
import pytest

from pyoppversion import OppVersion
from pyoppversion.consts import OppVersionChannel, OppVersionSource
from pyoppversion.exceptions import OppVersionInputException
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
async def test_stable_version(OppVersion):
    """Test docker stable."""
    with patch(
        "pyoppversion.docker.OppVersionDocker.data",
        fixture("docker/default"),
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(session=session, source=OppVersionSource.DOCKER)
            await oppversion.get_version()
            assert oppversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(OppVersion):
    """Test docker beta."""
    with patch(
        "pyoppversion.docker.OppVersionDocker.data",
        fixture("docker/default"),
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(
                session=session,
                source=OppVersionSource.DOCKER,
                channel=OppVersionChannel.BETA,
            )
            await oppversion.get_version()
            assert oppversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_beta_version(OppVersion):
    """Test docker beta."""
    with patch(
        "pyoppversion.docker.OppVersionDocker.data",
        fixture("docker/default"),
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(
                session=session,
                source=OppVersionSource.DOCKER,
                channel=OppVersionChannel.DEV,
            )
            await oppversion.get_version()
            assert oppversion.version == DEV_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(OppVersion):
    """Test docker stable during beta week."""
    with patch(
        "pyoppversion.docker.OppVersionDocker.data",
        fixture("docker/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(
                session=session,
                source=OppVersionSource.DOCKER,
            )
            await oppversion.get_version()
            assert oppversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(OppVersion):
    """Test docker beta during beta week."""
    with patch(
        "pyoppversion.docker.OppVersionDocker.data",
        fixture("docker/beta_week"),
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(
                session=session,
                source=OppVersionSource.DOCKER,
                channel=OppVersionChannel.BETA,
            )
        await oppversion.get_version()
        assert oppversion.version == BETA_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_stable_version_pagination(aresponses):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/openpeerpower/tags",
        "get",
        aresponses.Response(
            text=fixture("docker/page1", False), status=200, headers=HEADERS
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/openpeerpower/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("docker/page2", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        oppversion = OppVersion(
            session=session,
            source=OppVersionSource.DOCKER,
        )
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version_pagination(aresponses):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/openpeerpower/tags",
        "get",
        aresponses.Response(
            text=fixture("docker/page1", False), status=200, headers=HEADERS
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/openpeerpower/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("docker/page2", False), status=200, headers=HEADERS
        ),
    )
    async with aiohttp.ClientSession() as session:
        oppversion = OppVersion(
            session=session,
            source=OppVersionSource.DOCKER,
            channel=OppVersionChannel.BETA,
        )
        await oppversion.get_version()
        assert oppversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week_pagination(aresponses):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/openpeerpower/tags",
        "get",
        aresponses.Response(
            text=fixture("docker/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/openpeerpower/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("docker/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        oppversion = OppVersion(
            session=session,
            source=OppVersionSource.DOCKER,
        )
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week_pagination(aresponses):
    """Test docker beta during beta week."""
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/openpeerpower/tags",
        "get",
        aresponses.Response(
            text=fixture("docker/beta_week_page1", False),
            status=200,
            headers=HEADERS,
        ),
    )
    aresponses.add(
        "registry.hub.docker.com",
        "/v2/repositories/openpeerpower/openpeerpower/tags/page2",
        "get",
        aresponses.Response(
            text=fixture("docker/beta_week_page2", False),
            status=200,
            headers=HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        oppversion = OppVersion(
            session=session,
            source=OppVersionSource.DOCKER,
            channel=OppVersionChannel.BETA,
        )
        await oppversion.get_version()
        assert oppversion.version == BETA_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_input_exception(OppVersion):
    with pytest.raises(OppVersionInputException):
        OppVersion(source=OppVersionSource.DOCKER)
