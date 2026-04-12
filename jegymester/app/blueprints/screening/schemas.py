from marshmallow import Schema, fields


class ScreeningListSchema(Schema):
    id = fields.Integer()
    movie_id = fields.Integer()
    theater_id = fields.Integer()
    start_time = fields.DateTime()


class ScreeningRequestSchema(Schema):
    movie_id = fields.Integer(required=True)
    theater_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)


class ScreeningResponseSchema(ScreeningListSchema):
    pass


class ScreeningUpdateSchema(Schema):
    movie_id = fields.Integer()
    theater_id = fields.Integer()
    start_time = fields.DateTime()


class ScreeningMovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()


class ScreeningTheaterSchema(Schema):
    id = fields.Integer()
    theatname = fields.String()


class ScreeningDetailSchema(Schema):
    id = fields.Integer()
    start_time = fields.DateTime()
    movie = fields.Nested(ScreeningMovieSchema)
    theater = fields.Nested(ScreeningTheaterSchema)