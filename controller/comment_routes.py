from setup import db
from flask import jsonify, request, Blueprint
from model.movie import Movie
from model.comment import Comment

comments = Blueprint('comments', __name__)


@comments.post('/movies/<int:movie_id>/comments/add')
def add_comment_to_movie(movie_id):
    comment_data = request.json
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return jsonify('No movie with this id'), 409
    movie.comments.append(Comment(**comment_data))
    db.session.add(movie)
    db.session.commit()

    return jsonify('Added a comment to film')


@comments.delete('/comments/<int:comment_id>/remove')
def remove_comment(comment_id):
    comment_to_delete = Comment.query.filter_by(id=comment_id).first()
    if not comment_to_delete:
        return jsonify('Wrong comment id - nothing was deleted'), 404
    db.session.delete(comment_to_delete)
    db.session.commit()

    return jsonify(f'{comment_to_delete} - was removed')
