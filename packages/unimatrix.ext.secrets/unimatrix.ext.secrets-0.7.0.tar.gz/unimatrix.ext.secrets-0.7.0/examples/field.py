# pylint: skip-file
import marshmallow

import unimatrix.ext.secrets as secrets


class ExampleSchema(marshmallow.Schema):
    value = secrets.SecretField()


if __name__ == '__main__':
    schema = ExampleSchema()

    dto = schema.load({
        'value': {
            'provider': 'azure',
            'name': 'example-secret',
            'encoding': 'utf-8',
            'opts': {'vault': 'unimatrixdev'}
        }
    })

    print(dto)
