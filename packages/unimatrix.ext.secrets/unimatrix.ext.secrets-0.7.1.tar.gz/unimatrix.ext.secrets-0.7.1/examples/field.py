# pylint: skip-file
import marshmallow

import unimatrix.ext.secrets as secrets


class ExampleSchema(marshmallow.Schema):
    value = secrets.SecretField()


if __name__ == '__main__':
    schema = ExampleSchema()

    dto = schema.load({
        'value': {
            'provider': 'config',
            'opts': {'value': 'Inline secret'}
        }
    })

    print(dto)
