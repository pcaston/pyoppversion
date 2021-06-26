import asyncio
from socket import gaierror
from unittest.mock import patch

import pytest
from aiohttp import ClientError

from pyopversion import OpVersion
from pyopversion.exceptions import OpVersionFetchException, OpVersionParseException


@pytest.mark.asyncio
async def test_timeout_exception():
    async def mocked_fetch_TimeoutError(_args):
        raise asyncio.TimeoutError

    with patch("pyopversion.local.OpVersionLocal.fetch", mocked_fetch_TimeoutError):
        opversion = OpVersion()
        with pytest.raises(OpVersionFetchException):
            await opversion.get_version()


@pytest.mark.asyncio
async def test_fetch_exception():
    opversion = OpVersion()

    async def mocked_fetch_ImportError(_args):
        raise ImportError

    async def mocked_fetch_ModuleNotFoundError(_args):
        raise ModuleNotFoundError

    async def mocked_fetch_gaierror(_args):
        raise gaierror

    async def mocked_fetch_ClientError(_args):
        raise ClientError

    with patch("pyopversion.local.OpVersionLocal.fetch", mocked_fetch_ImportError):
        with pytest.raises(OpVersionFetchException):
            await opversion.get_version()

    with patch(
        "pyopversion.local.OpVersionLocal.fetch", mocked_fetch_ModuleNotFoundError
    ):
        with pytest.raises(OpVersionFetchException):
            await opversion.get_version()

    with patch("pyopversion.local.OpVersionLocal.fetch", mocked_fetch_gaierror):
        with pytest.raises(OpVersionFetchException):
            await opversion.get_version()

    with patch("pyopversion.local.OpVersionLocal.fetch", mocked_fetch_ClientError):
        with pytest.raises(OpVersionFetchException):
            await opversion.get_version()


@pytest.mark.asyncio
async def test_parse_exception():
    opversion = OpVersion()

    async def mocked_fetch(_args):
        pass

    def mocked_parse_KeyError(_args):
        raise KeyError

    def mocked_parse_TypeError(_args):
        raise TypeError

    with patch("pyopversion.local.OpVersionLocal.fetch", mocked_fetch):
        with patch("pyopversion.local.OpVersionLocal.parse", mocked_parse_KeyError):
            with pytest.raises(OpVersionParseException):
                await opversion.get_version()

        with patch("pyopversion.local.OpVersionLocal.parse", mocked_parse_TypeError):
            with pytest.raises(OpVersionParseException):
                await opversion.get_version()
