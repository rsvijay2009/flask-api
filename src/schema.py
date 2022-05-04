from marshmallow import Schema, fields, ValidationError


class UsersSchema(Schema):

    def validate_length(val):
        if len(val) < 2:
            raise ValidationError(
                f"Value must have 2 or more characters.")

    first_name = fields.Str(required=True)
    last_name = fields.String(required=True, validate=[
                              validate_length])
    email = fields.Email()
    password = fields.Str(required=True)
    mobile = fields.Integer(required=True)
