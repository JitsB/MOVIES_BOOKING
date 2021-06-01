from models import City, Theatre, Movie
from app import db
from sqlalchemy import and_

#Why the need of classes ?
class CityRepository:
    """ The repository for the city model """

    def getAllCities():
        cities =  City.query.all()
        cities = [vars(city)["city_name"] for city in cities]
        return cities
    
    def getCity(name):
        return City.query.filter_by(city_name=name).first()


class TheatreRepository:
    """ The repository for the theatre model """

    def getAllMovies(id):
        return Theatre.query.filter_by(t_city_id=id).all()
    
    def getTheatresShowingMovie(city_name, movie):
        city = CityRepository.getCity(city_name)
        if not city:
            return None
        
        city_id = vars(city)['city_id']

        output_theatres = []
        theatres = Theatre.query.filter_by(t_city_id=city_id).all()

        # output_theatres = [{"Name": t['theatre_name'],"Price": t['price'],"Total Seats":t['total_seats'],"Available Seats":t['total_seats']-t['booked_seats']} for t in theatres if movie in vars(t)['movies_playing']]
        for t in theatres:
            t = vars(t)
            if movie in t['movies_playing']:
                output_theatres.append({"Name": t['theatre_name'],"Price": t['price'],"Total Seats":t['total_seats'],"Available Seats":t['total_seats']-t['booked_seats']})
        
        return output_theatres

class MovieRepository:
    """ The repository for the movie model """

    def getAllMoviesForCity(city_name):
        city = CityRepository.getCity(city_name)
        if not city:
            return None

        city_id = vars(city)['city_id']
        
        theatres = TheatreRepository.getAllMovies(city_id)
        movies_playing = [vars(t)['movies_playing'] for t in theatres]
    
        return movies_playing