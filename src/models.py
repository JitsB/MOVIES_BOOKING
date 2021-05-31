from app import db

class City(db.Model):
    """ The City model """

    __tablename__ = "city"

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(300))
    city_state = db.Column(db.String(300))


class Theatre(db.Model):
    """ The Theatre model """

    __tablename__ = "theatre"

    theatre_id = db.Column(db.Integer, primary_key=True)
    theatre_name = db.Column(db.String(300))
    
    movies_playing = db.Column(db.String(300))
    total_seats = db.Column(db.Integer)

    booked_seats = db.Column(db.Integer)
    price = db.Column(db.Integer)

    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'))

    theatre = db.relationship('Theatre', backref='city')



class Movie(db.Model):
    """ The Movie model """

    __tablename__ = "movie"

    movie_name = db.Column(db.String(300), primary_key=True)

    movie_cast = db.Column(db.String(300))
    movie_screen_time = db.Column(db.Integer)

    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.theatre_id'))
    movie = db.relationship('movie', backref='theatre')

    city_name = db.Column(db.String(300))
    city_state = db.Column(db.String(300))



if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("Done!")