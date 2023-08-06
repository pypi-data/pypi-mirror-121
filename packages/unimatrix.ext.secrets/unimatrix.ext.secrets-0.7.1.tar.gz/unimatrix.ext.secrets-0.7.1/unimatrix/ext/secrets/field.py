"""Declares :class:`SecretField`."""
import marshmallow.fields

from .schema import SecretSchema


class SecretField(marshmallow.fields.Dict):
    """Field that deserializes the input parameters and uses them to fetch
    a secret from the secret storage backend.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        raise NotImplementedError

    def _deserialize(self, *args, **kwargs):
        schema = SecretSchema()
        secret = schema.load(super()._deserialize(*args, **kwargs))
        return secret[None]
