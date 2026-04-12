from marshmallow import Schema, fields


class TicketListSchema(Schema):
    id = fields.Integer()
    screening_id = fields.Integer()
    user_id = fields.Integer()
    ticketcategory_id = fields.Integer()
    seat_id = fields.Integer()


class TicketRequestSchema(Schema):
    screening_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    ticketcategory_id = fields.Integer(required=True)
    seat_id = fields.Integer(required=True)


class TicketResponseSchema(TicketListSchema):
    pass


class TicketUpdateSchema(Schema):
    screening_id = fields.Integer()
    user_id = fields.Integer()
    ticketcategory_id = fields.Integer()
    seat_id = fields.Integer()


class TicketDetailSchema(Schema):
    id = fields.Integer()
    screening = fields.Dict()
    user = fields.Dict()
    ticketcategory = fields.Dict()
    seat = fields.Dict()