# pylint: skip-file
import asyncio

import unimatrix.ext.secrets as secrets


async def main():
    print (await secrets.fetch('local', 'pki/pkcs/noop.rsa', {}))

    print (await secrets.fetch('config', None, {
        'value': 'Inline secret!'
    }))
    print (await secrets.fetch('azure', 'example-secret', {
        'vault': 'unimatrixdev',
    }))
    print (await secrets.fetch('google', 'EXAMPLE_SECRET', {
        'project': 'unimatrixdev',
    }))


if __name__ == '__main__':
    asyncio.run(main())
