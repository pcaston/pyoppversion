"""Example usage of pyopversion."""
import asyncio

import aiohttp

from pyopversion import OpVersion
from pyopversion.consts import OpVersionChannel, OpVersionSource


async def example():
    """Example usage of pyopversion."""
    async with aiohttp.ClientSession() as session:
        sources = [
            OpVersionSource.SUPERVISOR,
            OpVersionSource.PYPI,
        ]
        for source in sources:
            version, data = await OpVersion(
                session=session,
                source=source,
                board="generic-x86-64",
                channel=OpVersionChannel.DEFAULT,
            ).get_version()
            print(source)
            print("Version:", version)
            print("Version data:", data)
            print()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
