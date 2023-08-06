"""Declares :class:`ConfigProvider`."""
import marshmallow.fields

from .base import Provider
from .schema import BaseSchema


class ConfigProvider(Provider):
    """Secret storage implementation that uses the in-memory configuration as a
    storage backend.
    """

    class schema_class(BaseSchema):
        value = marshmallow.fields.String(required=True)

    def get_secret_version_sync(self, secret: 'Secret', version: str) -> bytes:
        return str.encode(secret.opts.value, 'utf-8')

    async def get_secret_version(self, secret: 'Secret', version: str =None):
        return str.encode(secret.opts.value, 'utf-8')
