from marshmallow import Schema, fields
from marshmallow.validate import Length


class UserRequestSchema(Schema):
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    password = fields.String(required=True, validate=Length(min=6))


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserUpdateSchema(Schema):
    email = fields.Email()
    phone = fields.String()
    password = fields.String(validate=Length(min=6))


class UserRoleSchema(Schema):
    id = fields.Integer()
    rolename = fields.String()


class UserTicketSchema(Schema):
    id = fields.Integer()
    screening_id = fields.Integer()
    ticketcategory_id = fields.Integer()
    seat_id = fields.Integer()


class UserResponseSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    phone = fields.String()


class UserListSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    phone = fields.String()


class UserDetailSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    phone = fields.String()
    roles = fields.List(fields.Nested(UserRoleSchema))
    tickets = fields.List(fields.Nested(UserTicketSchema))