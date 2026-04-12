from marshmallow import Schema, fields


class TheaterListSchema(Schema):
    id = fields.Integer()
    theatname = fields.String()


class TheaterRequestSchema(Schema):
    theatname = fields.String(required=True)


class TheaterResponseSchema(TheaterListSchema):
    pass


class TheaterUpdateSchema(Schema):
    theatname = fields.String()


class TheaterSeatSchema(Schema):
    id = fields.Integer()
    seat_number = fields.String()
    reserved = fields.Boolean()


class TheaterToSeatSchema(Schema):
    id = fields.Integer()
    theatname = fields.String()
    seats = fields.List(fields.Nested(TheaterSeatSchema))