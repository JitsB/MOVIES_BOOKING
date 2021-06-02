from models import City, Theatre, Movie
from app import db, engine
from sqlalchemy import text
import datetime






#Why the need of classes ?
class CityRepository:
    """ The repository for the city model """

    def getAllCities():
        
        result = engine.execute(
            text(
                "SELECT * from city;"
                )
            )
        cities = [dict(row) for row in result.fetchall()]
        return cities
    
    def getCity(name):
        result = engine.execute(
            text(
                "SELECT * from city where city_name = :name"
                )
            )
        cities = [dict(row) for row in result.fetchall()]
        print("Cities: ",cities)
        return cities
        
        # return session.query(City).filter_by(city_name=name).first()
    
    def getCityID(city_name):
        s = text(
                "SELECT city_id from city where city_name = :city_name"
                )
        result = engine.execute(s, city_name = city_name)
        city = dict(result.fetchall()[0])
        # city = [dict(row) for row in result.fetchall()]
        print("city: ",city)
        return city['city_id']


class TheatreRepository:
    """ The repository for the theatre model """

    def getTheatreByName(name):
        print("Theatre passed: ",name)
        s = text(
                "SELECT * from theatre where theatre_name = :name"
                )
        
        result = engine.execute(s, name=name)
        theatres = [dict(row) for row in result.fetchall()]
        print("Theatres: ",theatres)
        return theatres
        
    def getTheatreByID(id):
        s = text(
            "SELECT * from theatre where theatre_id = :id"
            )
        
        result = engine.execute(s, id=id)
        theatres = [dict(row) for row in result.fetchall()]
        return theatres

    def getTheatreForCity(city_id):
        s = text(
            "SELECT * from theatre where t_city_id = :city_id"
            )
    
        result = engine.execute(s, city_id = city_id)
        theatres = [dict(row) for row in result.fetchall()]
        return theatres

        return session.query(Theatre).filter_by(t_city_id=id).all()
    
    def getTheatresShowingMovie(city_id):
        
        s = text(
                "SELECT * from theatre where t_city_id = :city_id"
                )
        
        result = engine.execute(s, city_id=city_id)
        theatres = [dict(row) for row in result.fetchall()]
        
        return theatres
        
class MovieRepository:
    """ The repository for the movie model """

    def getSeatsForMovie(movie_name, theatre_id):
        s = text(
            "select total_seats from movie where movie_name = :movie and m_theatre_id = :theatre_id"
        )
        result = engine.execute(s, movie = movie_name, theatre_id = theatre_id)
        return dict(result.fetchall()[0])['total_seats']
        # noSeats_available = [dict(row)['total_seats'] for row in result.fetchall()]
        # return noSeats_available

    def getAllMoviesForCity(city_name):
        city_id = CityRepository.getCityID(city_name)
        print("City_id: ",city_id)
        theatres = TheatreRepository.getTheatresShowingMovie(city_id)
        print("theatres: ",theatres)
        movies = []
        for t in theatres:
            s = text(
                "SELECT * from movie where m_theatre_id = :theatre_id"
                )
            result = engine.execute(s, theatre_id = t['theatre_id'])
            # movies.append(dict(row) for row in result.fetchall())
            for row in result.fetchall():
                movies.append(dict(row))

        return movies
    
    def getTheatresForCityMovie(city_name, movie_n): # Change this to perform queries using text !
        city_id = CityRepository.getCityID(city_name)

        theatres = TheatreRepository.getTheatresShowingMovie(city_id)
        print("Theatres: ",theatres)
        output_theatres = []
        for t in theatres:
            s = text(
                "select * from theatre where theatre_id = (select m_theatre_id from movie where movie_name = :name and m_theatre_id = :id)"
            )
            result = engine.execute(s, name=movie_n, id=t["theatre_id"])
            for row in result.fetchall():
                output_theatres.append(dict(row))
            # output_theatres.append(dict(row) for row in result.fetchall())

            # theatre_id = vars(session.query(Movie).filter_by(movie_name = movie_n).filter_by(m_theatre_id = vars(t)['theatre_id']).first())['m_theatre_id']
            # output_theatres.append(vars(TheatreRepository.getTheatreByID(theatre_id))['theatre_name'])

        print("Output: ",output_theatres)
        return output_theatres

    

class BookingRepository:

    def createBooking(city, movie, theatre, seatsToBook):
        print("Inside create booking")
        city_id = CityRepository.getCityID(city)
        print("City_id: ",city_id)

        theatres = TheatreRepository.getTheatreByName(theatre)
        if not theatres:
            return None

        theatre_id = theatres[0]["theatre_id"]
        user_id = 1
        
        noSeats_available = MovieRepository.getSeatsForMovie(movie, theatre_id)
        print("No Seats available: ",noSeats_available)
        if int(seatsToBook) > noSeats_available:
            return -1
        print("Going inside transaction")

        with engine.begin() as conn:
            s = text(
                "update movie set total_seats = total_seats - :seatsToBook where movie_name = :movie and m_theatre_id = :theatre_id"
            )
            conn.execute(s, seatsToBook = seatsToBook, movie=movie, theatre_id = theatre_id)
            
            s = text(
                "insert into booking (b_user_id, b_city_id, b_theatre_id, movie_name, booked_seats, created_time) values(:user_id, :city_id, :theatre_id, :movie_name, :noSeats, :time)"
            )
            conn.execute(s, user_id = user_id, city_id = city_id, theatre_id = theatre_id, movie_name = movie, noSeats = seatsToBook, time = datetime.datetime.now())
        
        print("Transaction finished")
        return 1
