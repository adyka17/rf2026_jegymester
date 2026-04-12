class TicketOrderListSchema(Schema):
    order_id = fields.Integer()
    ticket_id = fields.Integer()
    ticket_status = fields.String()


class TicketOrderRequestSchema(Schema):
    order_id = fields.Integer(required=True)
    ticket_id = fields.Integer(required=True)
    ticket_status = fields.String(required=True)


class TicketOrderResponseSchema(TicketOrderListSchema):
    pass


class TicketOrderUpdateSchema(Schema):
    ticket_status = fields.String()
