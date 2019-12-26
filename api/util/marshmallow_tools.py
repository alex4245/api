from flask import request, g
from marshmallow import ValidationError
import json


def ma_validation(schema):
    def wrap(func):
        def wrapper(*args):
            data = json.loads(request.data)
            result = schema().load(data)
            if result.errors:
                raise ValidationError(u'Validation error')
            g.post_parametrs = result.data
            func(args)
        return wrapper
    return wrap
