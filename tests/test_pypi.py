"""Tests for PyPi."""

import json

import aiohttp
import pytest
from pyoppversion import PyPiVersion
from .const import (
    HEADERS,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
)
from .fixtures.fixture_pypi import pypi_response, pypi_response_beta_week


@pytest.mark.asyncio
async def test_stable_version(aresponses, event_loop, pypi_response):
    """Test pypi stable."""
    aresponses.add(
        "pypi.org",
        "/pypi/openpeerpower/json",
        "get",
        aresponses.Response(
            text=json.dumps(pypi_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        oppversion = PyPiVersion(event_loop, session)
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(aresponses, event_loop, pypi_response):
    """Test pypi beta."""
    aresponses.add(
        "pypi.org",
        "/pypi/openpeerpower/json",
        "get",
        aresponses.Response(
            text=json.dumps(pypi_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        oppversion = PyPiVersion(event_loop, session, "beta")
        await oppversion.get_version()
        assert oppversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(
    aresponses, event_loop, pypi_response_beta_week
):
    """Test pypi stable during beta week."""
    aresponses.add(
        "pypi.org",
        "/pypi/openpeerpower/json",
        "get",
        aresponses.Response(
            text=json.dumps(pypi_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        oppversion = PyPiVersion(event_loop, session)
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(aresponses, event_loop, pypi_response_beta_week):
    """Test pypi beta during beta week."""
    aresponses.add(
        "pypi.org",
        "/pypi/openpeerpower/json",
        "get",
        aresponses.Response(
            text=json.dumps(pypi_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        oppversion = PyPiVersion(event_loop, session, "beta")
        await oppversion.get_version()
        assert oppversion.version == "9.99.9b12"
