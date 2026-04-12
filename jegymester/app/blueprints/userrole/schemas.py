from marshmallow import Schema, fields


class UserRoleListSchema(Schema):
    user_id = fields.Integer()
    role_id = fields.Integer()


class UserRoleRequestSchema(Schema):
    user_id = fields.Integer(required=True)
    role_id = fields.Integer(required=True)


class UserRoleResponseSchema(UserRoleListSchema):
    pass


class UserRoleUpdateSchema(Schema):
    new_role_id = fields.Integer(required=True)