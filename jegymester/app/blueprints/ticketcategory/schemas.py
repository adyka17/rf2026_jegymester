from marshmallow import Schema, fields


class TicketCategoryListSchema(Schema):
    id = fields.Integer()
    catname = fields.String()
    price = fields.Integer()


class TicketCategoryRequestSchema(Schema):
    catname = fields.String(required=True)
    price = fields.Integer(required=True)


class TicketCategoryResponseSchema(TicketCategoryListSchema):
    pass


class TicketCategoryUpdateSchema(Schema):
    catname = fields.String()
    price = fields.Integer()
