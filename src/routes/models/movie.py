from . import db
from .theatre import Theatre

class Movie(db.Model):
    """ The Movie model """

    __tablename__ = "movie"

    movie_name = db.Column(db.String(300), primary_key=True)

    movie_cast = db.Column(db.String(300))
    movie_screen_time = db.Column(db.Integer)

    theatre_id = db.Column(Integer, ForeignKey('Theatre.theatre_id'), ondelete='CASCADE')
    movie = relationship('movie', backref='theatre')

    # city_name = db.Column(db.String(300))
    # city_state = db.Column(db.String(300))