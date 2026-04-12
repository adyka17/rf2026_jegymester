from app.extensions import db
from app.models.movie import Movie
from app.blueprints.movie.schemas import (
    MovieListSchema,
    MovieResponseSchema,
    MovieToScreeningSchema,
)
from sqlalchemy import select


class MovieService:
    @staticmethod
    def movie_list_all():
        movies = db.session.execute(select(Movie)).scalars().all()
        return True, MovieListSchema(many=True).dump(movies)

    @staticmethod
    def movie_get_item(item_id: int):
        movie = db.session.get(Movie, item_id)
        if not movie:
            return False, "A film nem található!"
        return True, MovieResponseSchema().dump(movie)

    @staticmethod
    def movie_add(data: dict):
        try:
            movie = Movie(**data)
            db.session.add(movie)
            db.session.commit()
            return True, MovieResponseSchema().dump(movie)
        except Exception:
            db.session.rollback()
            return False, "movie_add() hiba!"

    @staticmethod
    def movie_update(item_id: int, data: dict):
        movie = db.session.get(Movie, item_id)
        if not movie:
            return False, "A film nem található!"

        try:
            for field in ["title", "duration", "genre", "age_limit", "description"]:
                if field in data:
                    setattr(movie, field, data[field])

            db.session.commit()
            return True, MovieResponseSchema().dump(movie)
        except Exception:
            db.session.rollback()
            return False, "movie_update() hiba!"

    @staticmethod
    def movie_delete(item_id: int):
        movie = db.session.get(Movie, item_id)
        if not movie:
            return False, "A film nem található!"

        try:
            db.session.delete(movie)
            db.session.commit()
            return True, {"message": "A film törölve."}
        except Exception:
            db.session.rollback()
            return False, "movie_delete() hiba!"

    @staticmethod
    def movie_screenings(item_id: int):
        movie = db.session.get(Movie, item_id)
        if not movie:
            return False, "A film nem található!"

        payload = {
            "id": movie.id,
            "title": movie.title,
            "duration": movie.duration,
            "genre": movie.genre,
            "age_limit": movie.age_limit,
            "description": movie.description,
            "screenings": [
                {
                    "id": screening.id,
                    "theater_id": screening.theater_id,
                    "start_time": screening.start_time,
                }
                for screening in movie.screenings
            ],
        }
        return True, MovieToScreeningSchema().dump(payload)