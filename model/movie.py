from setup import db
from .movie_actor import movies_actors


class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    image_url = db.Column(db.Text(), nullable=True)
    rating = db.Column(db.Float(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    facts = db.Column(db.Text(), nullable=True)
    comments = db.relationship('Comment', backref="movie", lazy='dynamic', cascade="all,delete")
    actors = db.relationship("Actor", secondary=movies_actors, back_populates="movies")

    def __init__(self, rating=None, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)
        self.set_rating(rating)

    def set_rating(self, rating: float):
        if rating:
            if 0 < rating < 100:
                self.rating = rating
            else:
                raise AttributeError
        else:
            return None

    def __repr__(self):
        return f'Movie({self.id}) :  {self.title}'
