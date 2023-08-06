# pylint: skip-file
import asyncio

import unimatrix.ext.secrets as secrets


if __name__ == '__main__':

    coro = secrets.fetch('google', 'EXAMPLE_SECRET', {
        'project': 'unimatrixdev'
    })
    print( asyncio.run(coro) )
