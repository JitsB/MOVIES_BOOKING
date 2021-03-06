from models import City, Theatre, Movie
from config import db, engine
from sqlalchemy import text
import datetime


class CityRepository:
    """ The repository for the city model """

    def getAllCities(): #Get all cities present in the DB
        result = engine.execute(
            text(
                "SELECT * from city;"
                )
            )
        rows = result.fetchall()
        if len(rows) == 0:
            return None
        cities = [dict(row) for row in rows]
        return cities
    
    def getCityByName(name): #Get cities by their name
        s = text(
                "SELECT * from city where city_name = :name"
                )
            
        result = engine.execute(s, name = name)
        rows = result.fetchall()
        if len(rows) == 0:
            return None
        
        city = [dict(row) for row in rows]
        return cities
        
    def getCityID(city_name): # Get a city by its ID
        s = text(
                "SELECT city_id from city where city_name = :city_name"
                )
        result = engine.execute(s, city_name = city_name)
        
        rows = result.fetchall()
        if len(rows) == 0:
            return None
        
        city = dict(rows[0])
        return city['city_id']


class TheatreRepository:
    """ The repository for the theatre model """

    def getAllTheatres(): #Get all theatres
        result = engine.execute(
            text(
                "SELECT * from theatre;"
                )
            )
        rows = result.fetchall()
        if len(rows) == 0:
            return None

        theatres = [dict(row) for row in rows]
        return theatres

    def getTheatreByName(name): # Get theatres by name
        
        s = text(
                "SELECT * from theatre where theatre_name = :name"
                )
        result = engine.execute(s, name=name)
        rows = result.fetchall()
        if len(rows) == 0:
            return None
        theatres = [dict(row) for row in rows][0]
        
        return theatres
        

    def getTheatreByCityID(city_id): #Get theatres by city id
        s = text(
            "SELECT * from theatre where t_city_id = :city_id"
            )
    
        result = engine.execute(s, city_id = city_id)
        theatres = [dict(row) for row in result.fetchall()]
        return theatres
    
    def getTheatreByTheatreID(theatre_id, city_id): # Get theatre by theatre_id and city_id
        s = text(
            "select * from theatre where theatre_id = :t_id and t_city_id = :city_id"
        )
        result = engine.execute(s, t_id = theatre_id, city_id = city_id)
        result = [dict(row) for row in result.fetchall()]
        return result
        
class MovieRepository:
    """ The repository for the movie model """

    def getAllMovies(): #Get all movies
        result = engine.execute(
            text(
                "SELECT * from movie;"
                )
            )
        rows = result.fetchall()
        if len(rows) == 0:
            return None

        movies = [dict(row) for row in rows]
        return movies

    def getSeatsForMovie(movie_name, theatre_id): # Getting the no of seats available for a movie
        s = text(
            "select total_seats from movie where movie_name = :movie and m_theatre_id = :theatre_id"
        )
        result = engine.execute(s, movie = movie_name, theatre_id = theatre_id)
        return dict(result.fetchall()[0])['total_seats']
        
    def getAllMoviesForCity(city_name): # Get all movies playing in a city
        city_id = CityRepository.getCityID(city_name)
        
        theatres = TheatreRepository.getTheatreByCityID(city_id)
        movies = []
        for t in theatres:
            s = text(
                "SELECT * from movie where m_theatre_id = :theatre_id"
                )

            result = engine.execute(s, theatre_id = t['theatre_id'])
            for row in result.fetchall():
                movies.append(dict(row))

        return movies
    

    def getTheatresForCityMovie(city_name, movie_n): # Get Movies playing in a city in a specific theatre
        city_id = CityRepository.getCityID(city_name)

        theatres = TheatreRepository.getTheatreByCityID(city_id)
    
        output_theatres = []
        for t in theatres:
            s = text(
                "select * from theatre where theatre_id = (select m_theatre_id from movie where movie_name = :name and m_theatre_id = :id)"
            )
            result = engine.execute(s, name=movie_n, id=t["theatre_id"])
            for row in result.fetchall():
                output_theatres.append(dict(row))
            
        return output_theatres

    

class BookingRepository:

    def createBooking(city, movie, theatre, seatsToBook): # Book seats for a movie
        city_id = CityRepository.getCityID(city)

        theatre_id = TheatreRepository.getTheatreByName(theatre)['theatre_id']
        
        theatres = TheatreRepository.getTheatreByTheatreID(theatre_id, city_id)
        if not theatres:
            return None

        theatre_id = theatres[0]["theatre_id"]
        user_id = 1
        
        noSeats_available = MovieRepository.getSeatsForMovie(movie, theatre_id)
        if int(seatsToBook) > noSeats_available:
            return -1

        with engine.begin() as conn:
            s = text(
                "update movie set total_seats = total_seats - :seatsToBook where movie_name = :movie and m_theatre_id = :theatre_id"
            )
            conn.execute(s, seatsToBook = seatsToBook, movie=movie, theatre_id = theatre_id)
            
            s = text(
                "insert into booking (b_user_id, b_city_id, b_theatre_id, movie_name, booked_seats, created_time) values(:user_id, :city_id, :theatre_id, :movie_name, :noSeats, :time)"
            )
            result = conn.execute(s, user_id = user_id, city_id = city_id, theatre_id = theatre_id, movie_name = movie, noSeats = seatsToBook, time = datetime.datetime.now())
            id = result.lastrowid
        
        return id
