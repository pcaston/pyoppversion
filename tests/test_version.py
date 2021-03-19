import asyncio
from socket import gaierror
from unittest.mock import patch

import pytest
from aiohttp import ClientError

from pyoppversion import OppVersion
from pyoppversion.exceptions import OppVersionFetchException, OppVersionParseException


@pytest.mark.asyncio
async def test_timeout_exception():
    async def mocked_fetch_TimeoutError(_args):
        raise asyncio.TimeoutError

    with patch("pyoppversion.local.OppVersionLocal.fetch", mocked_fetch_TimeoutError):
        oppversion = OppVersion()
        with pytest.raises(OppVersionFetchException):
            await oppversion.get_version()


@pytest.mark.asyncio
async def test_fetch_exception():
    oppversion = OppVersion()

    async def mocked_fetch_ImportError(_args):
        raise ImportError

    async def mocked_fetch_ModuleNotFoundError(_args):
        raise ModuleNotFoundError

    async def mocked_fetch_gaierror(_args):
        raise gaierror

    async def mocked_fetch_ClientError(_args):
        raise ClientError

    with patch("pyoppversion.local.OppVersionLocal.fetch", mocked_fetch_ImportError):
        with pytest.raises(OppVersionFetchException):
            await oppversion.get_version()

    with patch(
        "pyoppversion.local.OppVersionLocal.fetch", mocked_fetch_ModuleNotFoundError
    ):
        with pytest.raises(OppVersionFetchException):
            await oppversion.get_version()

    with patch("pyoppversion.local.OppVersionLocal.fetch", mocked_fetch_gaierror):
        with pytest.raises(OppVersionFetchException):
            await oppversion.get_version()

    with patch("pyoppversion.local.OppVersionLocal.fetch", mocked_fetch_ClientError):
        with pytest.raises(OppVersionFetchException):
            await oppversion.get_version()


@pytest.mark.asyncio
async def test_parse_exception():
    oppversion = OppVersion()

    async def mocked_fetch(_args):
        pass

    def mocked_parse_KeyError(_args):
        raise KeyError

    def mocked_parse_TypeError(_args):
        raise TypeError

    with patch("pyoppversion.local.OppVersionLocal.fetch", mocked_fetch):
        with patch("pyoppversion.local.OppVersionLocal.parse", mocked_parse_KeyError):
            with pytest.raises(OppVersionParseException):
                await oppversion.get_version()

        with patch("pyoppversion.local.OppVersionLocal.parse", mocked_parse_TypeError):
            with pytest.raises(OppVersionParseException):
                await oppversion.get_version()
