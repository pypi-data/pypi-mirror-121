"""Declares :class:`SecretSchema`."""
import marshmallow
import marshmallow.fields

from .providers import get_valid_providers
from .providers import validate_opts
from .secret import Secret


class SecretSchema(marshmallow.Schema):
    """Validation schema to load secrets using providers."""
    provider = marshmallow.fields.String(
        required=True,
        validate=marshmallow.validate.OneOf(get_valid_providers())
    )

    name = marshmallow.fields.String(
        missing=None
    )

    alias = marshmallow.fields.String(
        required=False
    )

    encoding = marshmallow.fields.String(
        required=False,
        validate=marshmallow.validate.OneOf(['utf-8'])
    )

    opts = marshmallow.fields.Dict(
        required=False,
        missing=dict,
        default=dict,
        allow_none=True
    )

    def load(self, *args, **kwargs):
        dto = super().load(*args, **kwargs)
        dto['opts'] = validate_opts(dto['provider'], dto.get('opts') or {})
        return Secret(**dto)
