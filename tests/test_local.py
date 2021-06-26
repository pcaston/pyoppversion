"""Tests for ha.io/version.json."""
from unittest.mock import MagicMock, patch

import aiohttp
import pytest

from pyopversion import OpVersion
from pyopversion.consts import OpVersionSource

from .const import STABLE_VERSION


@pytest.mark.asyncio
async def test_local():
    """Test ha.io/version.json stable."""
    with patch.dict(
        "sys.modules", {"openpeerpower.const": MagicMock(__version__=STABLE_VERSION)}
    ):
        async with aiohttp.ClientSession() as session:
            opversion = OpVersion(session=session, source=OpVersionSource.LOCAL)
            await opversion.get_version()
            assert opversion.version == STABLE_VERSION
