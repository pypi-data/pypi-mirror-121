# pylint: skip-file
import asyncio

import unimatrix.ext.secrets as secrets


if __name__ == '__main__':
    secrets.add({
        'provider': 'config',
        'name': 'EXAMPLE_SECRET',
        'opts': {'value': 'Secret from config'}
    })

    print(asyncio.run(secrets.get('EXAMPLE_SECRET')))
