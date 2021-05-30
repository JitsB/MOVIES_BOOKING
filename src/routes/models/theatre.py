from . import db
from .city import City

class Theatre(db.Model):
    """ The Theatre model """

    __tablename__ = "theatre"

    theatre_id = db.Column(db.Integer, primary_key=True)
    theatre_name = db.Column(db.String(300))
    
    movies_playing = db.Column(db.String(300))
    total_seats = db.Column(db.Integer)

    booked_seats = db.Column(db.Integer)
    price = db.Column(db.Integer)

    city_id = db.Column(db.Integer, ForeignKey('city.city_id'), ondelete='CASCADE')

    theatre = relationship('Theatre', backref='city')

    # city_state = db.Column(db.String(300))