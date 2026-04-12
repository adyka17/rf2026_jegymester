from marshmallow import Schema, fields


class MovieListSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    duration = fields.Integer()
    genre = fields.String()
    age_limit = fields.Integer()
    description = fields.String()


class MovieRequestSchema(Schema):
    title = fields.String(required=True)
    duration = fields.Integer(required=True)
    genre = fields.String(required=True)
    age_limit = fields.Integer(required=True)
    description = fields.String(required=True)


class MovieResponseSchema(MovieListSchema):
    pass


class MovieUpdateSchema(Schema):
    title = fields.String()
    duration = fields.Integer()
    genre = fields.String()
    age_limit = fields.Integer()
    description = fields.String()


class MovieScreeningItemSchema(Schema):
    id = fields.Integer()
    theater_id = fields.Integer()
    start_time = fields.DateTime()


class MovieToScreeningSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    duration = fields.Integer()
    genre = fields.String()
    age_limit = fields.Integer()
    description = fields.String()
    screenings = fields.List(fields.Nested(MovieScreeningItemSchema))