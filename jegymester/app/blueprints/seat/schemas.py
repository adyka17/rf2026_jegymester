from marshmallow import Schema, fields


class SeatListSchema(Schema):
    id = fields.Integer()
    theater_id = fields.Integer()
    seat_number = fields.String()
    reserved = fields.Boolean()


class SeatRequestSchema(Schema):
    theater_id = fields.Integer(required=True)
    seat_number = fields.String(required=True)
    reserved = fields.Boolean(load_default=False)


class SeatResponseSchema(SeatListSchema):
    pass


class SeatUpdateSchema(Schema):
    theater_id = fields.Integer()
    seat_number = fields.String()
    reserved = fields.Boolean()