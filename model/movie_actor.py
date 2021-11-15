from setup import db

movies_actors = db.Table('movie_actor', db.Model.metadata,
                         db.Column('movie_id', db.ForeignKey('movie.id')),
                         db.Column('actor_id', db.ForeignKey('actor.id'))
                         )
