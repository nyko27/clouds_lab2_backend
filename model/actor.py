from setup import db
from .movie_actor import movies_actors


class Actor(db.Model):
    __tablename__ = "actor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    image_url = db.Column(db.Text(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    movies = db.relationship(
        "Movie",
        secondary=movies_actors,
        back_populates="actors")

    def __repr__(self):
        return f"<Actor({self.id}) - {self.name}>"
