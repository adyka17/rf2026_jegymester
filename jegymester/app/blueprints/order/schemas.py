from marshmallow import Schema, fields


class OrderListSchema(Schema):
    id = fields.Integer()
    payment_status = fields.String()


class OrderRequestSchema(Schema):
    payment_status = fields.String(required=True)


class OrderResponseSchema(OrderListSchema):
    pass


class OrderUpdateSchema(Schema):
    payment_status = fields.String()


class OrderDetailTicketSchema(Schema):
    ticket_id = fields.Integer()
    ticket_status = fields.String()


class OrderDetailSchema(Schema):
    id = fields.Integer()
    payment_status = fields.String()
    tickets = fields.List(fields.Nested(OrderDetailTicketSchema))