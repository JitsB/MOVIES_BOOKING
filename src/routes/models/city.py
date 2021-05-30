from . import db

class City(db.Model):
    """ The City model """

    __tablename__ = "city"

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(300))
    city_state = db.Column(db.String(300))