"""Declares :class:`ConfigProvider`."""
from .base import Provider


class ConfigProvider(Provider):
    """Secret storage implementation that uses the in-memory configuration as a
    storage backend.
    """

    def get_secret_version_sync(self, secret: 'Secret', version: str) -> bytes:
        return secret.opts.value

    async def get_secret_version(self, secret: 'Secret', version: str =None):
        return secret.opts.value
