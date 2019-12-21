from marshmallow import Schema, fields

class MaUserMainInfo(Schema):
    full_name = fields.Str(required=True)
    status = fields.Str()

