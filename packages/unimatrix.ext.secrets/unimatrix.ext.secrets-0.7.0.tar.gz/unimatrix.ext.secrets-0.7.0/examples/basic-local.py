# pylint: skip-file
import asyncio

import unimatrix.runtime
import unimatrix.ext.secrets as secrets


if __name__ == '__main__':
    asyncio.run(unimatrix.runtime.on('boot'))

    secrets.add({
        'provider': 'local',
        'name': 'pki/pkcs/noop.rsa',
        'alias': 'EXAMPLE_SECRET',
        'encoding': 'utf-8'
    })

    print(asyncio.run(secrets.get('EXAMPLE_SECRET')))
