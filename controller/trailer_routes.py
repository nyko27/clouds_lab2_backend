from flask import jsonify, Blueprint
from sqlalchemy import text
from setup import db


trailers = Blueprint('trailers', __name__)


@trailers.get('/trailers')
def get_trailers():
    result = db.engine.execute(text('select * from trailer'))
    columns = tuple(result.keys())
    trailers_data = tuple(row for row in result)

    response = []
    for row_data in trailers_data:
        response.append({column: value for column, value in zip(columns, row_data)})

    return jsonify(response)
