# pylint: skip-file
from .conf import load
from .field import SecretField
from .schema import SecretSchema
from .secret import Secret
from .registry import registry


__all__ = [
    'add',
    'fetch',
    'get',
    'get_sync',
    'load',
    'SecretField',
    'SecretSchema',
]


def add(params):
    """Adds a new secret to the secret registry."""
    registry.add(params)


async def fetch(provider: str, name: str, opts: dict, **kwargs) -> bytes:
    """Fetch secret `name` from the secret storage backend using the given
    provider `provider` with given options `opts`.
    """
    secret = Secret(provider, name, opts, **kwargs)
    return await secret.get(None)


def get_sync(name, version=None):
    """Retrieve a secret from the registry. Optionally
    `version` may be specified to indicate a version. If
    the `version` argument is omitted, then the latest
    version is returned.
    """
    return registry[name][version]


async def get(name, version=None):
    """Retrieve a secret from the registry. Optionally
    `version` may be specified to indicate a version. If
    the `version` argument is omitted, then the latest
    version is returned.
    """
    return await registry.get(name, version)
