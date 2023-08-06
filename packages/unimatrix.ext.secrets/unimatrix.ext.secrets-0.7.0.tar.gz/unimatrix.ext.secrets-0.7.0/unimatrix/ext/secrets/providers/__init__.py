# pylint: skip-file
import ioc.loader


__all__ = [
    'get_provider',
    'get_provider_class',
    'get_sync',
    'is_valid_provider',
]


PROVIDER_CLASSES = {
    'azure' : 'unimatrix.ext.secrets.providers.azure.AzureProvider',
    'config': 'unimatrix.ext.secrets.providers.config.ConfigProvider',
    'google': 'unimatrix.ext.secrets.providers.google.GoogleProvider',
    'local' : 'unimatrix.ext.secrets.providers.local.LocalProvider',
}


def is_valid_provider(kind: str) -> bool:
    """Return a boolean indicating if the provider kind is valid."""
    return kind in PROVIDER_CLASSES


def get_valid_providers() -> tuple:
    """Return the list of valid providers."""
    return tuple(PROVIDER_CLASSES.keys())


def get_provider_class(kind: str):
    """Return the provider of the given `kind`."""
    return ioc.loader.import_symbol(PROVIDER_CLASSES[kind])


def get_provider(kind: str):
    """Return a :class:`~unimatrix.ext.crypto.providers.Provider` instance
    of the given `kind`.
    """
    return get_provider_class(kind)()


def get_sync(secret, version=None):
    """Resolve the provider for `secret` :class:`~unimatrix.ext.secrets.Secret`
    and return secret content.
    """
    return get_provider(secret.provider)\
        .get_secret_version_sync(secret, version)


async def get(secret, version=None):
    """Resolve the provider for `secret` :class:`~unimatrix.ext.secrets.Secret`
    and return secret content.
    """
    return await get_provider(secret.provider)\
        .get_secret_version(secret, version)


def validate_opts(kind: str, opts: dict):
    """Use the schema specified on the provider class to validate the options
    configured for a secret.
    """
    Provider = get_provider_class(kind)
    schema = Provider.schema_class()
    return schema.load(opts)
