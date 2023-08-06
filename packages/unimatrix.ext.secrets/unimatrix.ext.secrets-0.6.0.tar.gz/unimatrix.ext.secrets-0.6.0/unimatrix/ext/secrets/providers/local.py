"""Declares :class:`LocalProvider`."""
import aiofiles

from .base import Provider


class LocalProvider(Provider):
    """Secret storage implementation that uses the local disk as a
    storage backend.
    """

    def get_secret_version_sync(self, secret: 'Secret', version: str) -> bytes:
        with open(secret.name, 'rb') as f:
            return f.read()

    async def get_secret_version(self, secret: 'Secret', version: str =None):
        async with aiofiles.open(secret.name, 'rb') as f:
            return await f.read()
