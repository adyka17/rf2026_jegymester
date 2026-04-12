from marshmallow import Schema, fields


class RoleListSchema(Schema):
    id = fields.Integer()
    rolename = fields.String()


class RoleRequestSchema(Schema):
    rolename = fields.String(required=True)


class RoleResponseSchema(RoleListSchema):
    pass


class RoleUpdateSchema(Schema):
    rolename = fields.String()