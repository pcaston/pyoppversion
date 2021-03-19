"""Tests for opp.io/version.json."""
from unittest.mock import MagicMock, patch

import aiohttp
import pytest

from pyoppversion import OppVersion
from pyoppversion.consts import OppVersionSource

from .const import STABLE_VERSION


@pytest.mark.asyncio
async def test_local():
    """Test opp.io/version.json stable."""
    with patch.dict(
        "sys.modules", {"openpeerpower.const": MagicMock(__version__=STABLE_VERSION)}
    ):
        async with aiohttp.ClientSession() as session:
            oppversion = OppVersion(session=session, source=OppVersionSource.LOCAL)
            await oppversion.get_version()
            assert oppversion.version == STABLE_VERSION
