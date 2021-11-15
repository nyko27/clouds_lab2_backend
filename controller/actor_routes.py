from flask import Blueprint, request, jsonify
from setup import db
from model.actor import Actor
from model.movie import Movie
from cfg.json_serializer import DbModelRelationshipSerializer
import json
from sqlalchemy.exc import IntegrityError

actors = Blueprint('actors', __name__, url_prefix='/actors')


@actors.get('/<int:actor_id>')
def get_actor_by(actor_id):
    actor = Actor.query.filter_by(id=actor_id).first()

    if not actor:
        return jsonify("No actor with such id"), 404

    return json.dumps(actor, cls=DbModelRelationshipSerializer)


@actors.post('/add')
def add_actor():
    actor_data = request.get_json()
    movies_to_add = actor_data.pop("movies", None)
    new_actor = Actor(**actor_data)

    if movies_to_add:
        for movie in movies_to_add[:]:
            if existing_movie := Movie.query.filter_by(title=movie).first():
                movies_to_add.remove(movie)
                new_actor.movies.append(existing_movie)

        new_movies = tuple(Movie(title=movie_title) for movie_title in movies_to_add)
        new_actor.movies.extend(new_movies)

    db.session.add(new_actor)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify('Actor was\'t added, because actor with the same name already exists'), 409

    return jsonify('Added a new actor')


@actors.patch('<int:actor_id>/update')
def update_actor(actor_id):
    actor_updated_data = request.get_json()

    if not (actor_to_update := Actor.query.filter_by(id=actor_id).first()):
        return jsonify('No actor with specified id - nothing was updated')

    for column_name, value in actor_updated_data.items():
        setattr(actor_to_update, column_name, value)

    db.session.commit()

    return jsonify('Actor was updated')


@actors.delete('/<int:actor_id>/remove')
def remove_actor(actor_id):
    actor_to_delete = Actor.query.filter_by(id=actor_id).first()
    if not actor_to_delete:
        return jsonify('Wrong actor id - nothing was deleted'), 404

    db.session.delete(actor_to_delete)
    db.session.commit()
    return jsonify(f'{actor_to_delete} was removed')
