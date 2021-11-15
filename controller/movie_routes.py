from cfg.json_serializer import DbModelRelationshipSerializer
import json
from setup import db
from flask import jsonify, request, Blueprint
from model.movie import Movie
from model.actor import Actor
from sqlalchemy.exc import IntegrityError

movies = Blueprint('movies', __name__, url_prefix='/movies')


@movies.get('')
def all_movies():
    queried_columns = ("id", "title", "image_url", "rating")
    columns_number = len(queried_columns)
    all_films = Movie.query.with_entities(*(eval(f'Movie.{column}') for column in queried_columns)).all()
    response = tuple(map(lambda row: dict((queried_columns[i], row[i]) for i in range(columns_number)), all_films))

    return jsonify(response)


@movies.get('/<int:movie_id>')
def get_movie_by(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        return jsonify("No movie with such id"), 404

    return json.dumps(movie, cls=DbModelRelationshipSerializer)


@movies.post('/add')
def add_movie():
    movie_data = request.get_json()
    actors_to_add = movie_data.pop("actors", None)

    try:
        new_movie = Movie(**movie_data)
    except AttributeError:
        return jsonify('Film rating must be from 0 to 100')

    if actors_to_add:
        for actor in actors_to_add[:]:
            if existing_actor := Actor.query.filter_by(name=actor).first():
                actors_to_add.remove(actor)
                new_movie.actors.append(existing_actor)

        new_actors = tuple(Actor(name=actor_name) for actor_name in actors_to_add)
        new_movie.actors.extend(new_actors)

    db.session.add(new_movie)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify('Movie was\'t added, because movie with the same title already exists')

    return jsonify('Added a new film')


@movies.patch('<int:movie_id>/update')
def update_movie(movie_id):
    movie_updated_data = request.get_json()
    print(movie_updated_data)
    if not (movie_to_update := Movie.query.filter_by(id=movie_id).first()):
        return jsonify('No movie with specified id - nothing was updated')

    for column_name, value in movie_updated_data.items():
        setattr(movie_to_update, column_name, value)

    db.session.commit()

    return jsonify('Film was updated')


@movies.delete('/<int:movie_id>/remove')
def remove_movie(movie_id):
    if not (movie_to_delete := Movie.query.filter_by(id=movie_id).first()):
        return jsonify('Wrong movie id - nothing was deleted'), 404

    db.session.delete(movie_to_delete)
    db.session.commit()
    return jsonify(f'{movie_to_delete} was removed')
