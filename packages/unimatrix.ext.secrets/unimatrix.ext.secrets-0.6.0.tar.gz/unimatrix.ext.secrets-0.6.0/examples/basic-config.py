# pylint: skip-file
import asyncio

import unimatrix.runtime
import unimatrix.ext.secrets as secrets


if __name__ == '__main__':
    asyncio.run(unimatrix.runtime.on('boot'))

    secrets.add({
        'provider': 'config',
        'name': 'EXAMPLE_SECRET',
        'encoding': 'utf-8',
        'opts': {'value': 'Secret from config'}
    })

    print(asyncio.run(secrets.get('EXAMPLE_SECRET')))
