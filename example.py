"""Example usage of pyoppversion."""
import asyncio

import aiohttp

from pyoppversion import OppVersion
from pyoppversion.consts import OppVersionBoard, OppVersionChannel, OppVersionSource


async def example():
    """Example usage of pyoppversion."""
    async with aiohttp.ClientSession() as session:
        sources = [
            OppVersionSource.DOCKER,
            OppVersionSource.SUPERVISED,
            OppVersionSource.OPPIO,
            OppVersionSource.PYPI,
        ]
        for source in sources:
            version, data = await OppVersion(
                session=session,
                source=source,
                channel=OppVersionChannel.DEFAULT,
                board=OppVersionBoard.DEFAULT,
            ).get_version()
            print(source)
            print("Version:", version)
            print("Version data:", data)
            print()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
