# pylint: skip-file
import unimatrix.ext.secrets as secrets


if __name__ == '__main__':
    schema = secrets.SecretSchema()

    print(schema.load({
        'provider': 'azure',
        'name': 'example-secret',
        'opts': {
            'vault': 'unimatrixdev',
        }
    }))

    print(schema.load({
        'provider': 'config',
        'name': None,
        'opts': {
            'value': "Inline secret!"
        }
    }))

    print(schema.load({
        'provider': 'google',
        'name': 'EXAMPLE_SECRET',
        'opts': {
            'project': 'unimatrixdev',
        }
    }))
