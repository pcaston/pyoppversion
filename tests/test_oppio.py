"""Tests for Oppio."""

import json

import aiohttp
import pytest
from pyoppversion import OppioVersion
from .const import (
    HEADERS,
    STABLE_VERSION,
    STABLE_VERSION_BETA_WEEK,
    BETA_VERSION,
    BETA_VERSION_BETA_WEEK,
)
from .fixtures.fixture_oppio import (
    oppio_response,
    oppio_response_beta_week,
    oppio_beta_response,
    oppio_beta_response_beta_week,
)


@pytest.mark.asyncio
async def test_stable_version(aresponses, event_loop, oppio_response):
    """Test oppio stable."""
    aresponses.add(
        "version.openpeerpower.io/",
        "/stable.json",
        "get",
        aresponses.Response(
            text=json.dumps(oppio_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        oppversion = OppioVersion(event_loop, session)
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION


@pytest.mark.asyncio
async def test_beta_version(aresponses, event_loop, oppio_beta_response):
    """Test oppio beta."""
    aresponses.add(
        "version.openpeerpower.io/",
        "/beta.json",
        "get",
        aresponses.Response(
            text=json.dumps(oppio_beta_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        oppversion = OppioVersion(event_loop, session, "beta")
        await oppversion.get_version()
        assert oppversion.version == BETA_VERSION


@pytest.mark.asyncio
async def test_stable_version_beta_week(
    aresponses, event_loop, oppio_response_beta_week
):
    """Test oppio stable during beta week."""
    aresponses.add(
        "version.openpeerpower.io/",
        "/stable.json",
        "get",
        aresponses.Response(
            text=json.dumps(oppio_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        oppversion = OppioVersion(event_loop, session)
        await oppversion.get_version()
        assert oppversion.version == STABLE_VERSION_BETA_WEEK


@pytest.mark.asyncio
async def test_beta_version_beta_week(
    aresponses, event_loop, oppio_beta_response_beta_week
):
    """Test oppio beta during beta week."""
    aresponses.add(
        "version.openpeerpower.io/",
        "/beta.json",
        "get",
        aresponses.Response(
            text=json.dumps(oppio_beta_response_beta_week), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        oppversion = OppioVersion(event_loop, session, "beta")
        await oppversion.get_version()
        assert oppversion.version == BETA_VERSION_BETA_WEEK
