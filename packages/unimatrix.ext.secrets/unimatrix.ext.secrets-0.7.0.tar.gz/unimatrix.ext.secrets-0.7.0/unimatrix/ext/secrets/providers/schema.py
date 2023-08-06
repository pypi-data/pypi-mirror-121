"""Declares :class:`BaseSchema`."""
import marshmallow
from unimatrix.lib.datastructures import ImmutableDTO


class BaseSchema(marshmallow.Schema):

    def load(self, *args, **kwargs):
        dto = super().load(*args, **kwargs)
        return ImmutableDTO.fromdict(dto)\
            if not self.many\
            else [ImmutableDTO.fromdict(x) for x in dto]
