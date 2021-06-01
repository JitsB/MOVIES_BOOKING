from models import City, Theatre, Movie
from app import db, engine
from sqlalchemy import text



# def remove_sa_instance()


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
        city = [dict(row) for row in result.fetchall()]
        print("City: ",city)
        
        return city[0]['city_id']


class TheatreRepository:
    """ The repository for the theatre model """

    def getTheatreByName(name):
        return session.query(Theatre).filter_by(theatre_name=name).first()
    
    def getTheatreByID(id):
        return session.query(Theatre).filter_by(theatre_id=id).first()

    def getTheatreForCity(city_id):
        return session.query(Theatre).filter_by(t_city_id=id).all()
    
    def getTheatresShowingMovie(city_id):
        
        s = text(
                "SELECT * from theatre where t_city_id = :city_id"
                )
        
        result = engine.execute(s, city_id=city_id)
        theatres = [dict(row) for row in result.fetchall()]
        print("theatres: ",theatres)
        # theatres = session.query(Theatre).filter_by(t_city_id=city_id).all()
        return theatres
        
class MovieRepository:
    """ The repository for the movie model """

    def getAllMoviesForCity(city_name):
        city_id = CityRepository.getCityID(city_name)
        
        theatres = TheatreRepository.getTheatresShowingMovie(city_id)
        movies = []
        for t in theatres:
            s = text(
                "SELECT * from movie where m_theatre_id = :theatre_id"
                )
            result = engine.execute(s, theatre_id = t['theatre_id'])
            movies.append(dict(row) for row in result.fetchall())
            
        return movies
    
    def getTheatresForCityMovie(city_name, movie_n): # Change this to perform queries using text !
        city_id = CityRepository.getCityID(city_name)

        theatres = TheatreRepository.getTheatresShowingMovie(city_id)
        
        output_theatres = []
        for t in theatres:
            theatre_id = vars(session.query(Movie).filter_by(movie_name = movie_n).filter_by(m_theatre_id = vars(t)['theatre_id']).first())['m_theatre_id']
            output_theatres.append(vars(TheatreRepository.getTheatreByID(theatre_id))['theatre_name'])

        print("Output: ",output_theatres)
        return output_theatres


    def checkAvailableSeats(city_name, theatre_name, movie, seats):
        return None
    
    def bookSeats(city_name, theatre_name, movie_n, seats):
        city_id = CityRepository.getCityID(city_name)

        theatre = TheatreRepository.getTheatre(theatre_name)
        if not theatre:
            return None

        theatre_id = vars(theatre)['theatre_id']
        #Do this in transaction, add validation 
        result = session.query(Movie).filter_by(m_theatre_id = theatre_id).filter_by(movie_name=movie_n).update({Movie.booked_seats: Movie.booked_seats + seats}, synchronize_session=False)
        session.commit()

        return result


class BookingRepository:

    def createBooking(city, movie, theatre, noSeats):
        city_id = CityRepository.getCityID(city_name)

        theatre = TheatreRepository.getTheatre(theatre_name)
        if not theatre:
            return None

        theatre_id = vars(theatre)['theatre_id']


        