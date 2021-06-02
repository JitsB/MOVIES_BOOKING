from app import db
import datetime

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
    
    t_city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'))
    theatre = db.relationship('City')


class Movie(db.Model):
    """ The Movie model """

    __tablename__ = "movie"

    movie_name = db.Column(db.String(300), primary_key=True) #Make it composite of name + theatreid

    movie_cast = db.Column(db.String(300))
    movie_screen_time = db.Column(db.Integer)

    total_seats = db.Column(db.Integer)
    booked_seats = db.Column(db.Integer)

    price = db.Column(db.Integer)

    m_theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.theatre_id'), primary_key=True) # Check if it actually creates a composite key ?
    movie = db.relationship('Theatre')


class User(db.Model):

    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(300))
    user_email = db.Column(db.String(300))


class Booking(db.Model):
    """ The Booking model """

    __tablename__ = "booking"

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    movie_name = db.Column(db.String(300))
    booked_seats = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    b_city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'))
    booking = db.relationship('City')

    b_theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.theatre_id'))
    booking = db.relationship('Theatre')

    b_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    booking = db.relationship('User')


#Add indexes

if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print("Creating database tables...")
    db.create_all()
    print("Done!")