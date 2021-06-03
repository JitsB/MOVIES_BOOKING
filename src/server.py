from config import app, db
from controller import CityRepository, MovieRepository, TheatreRepository, BookingRepository
from flask import Flask, jsonify, request, make_response


@app.route("/showCities",methods=["GET"])
def showCities():
    
    cities = CityRepository.getAllCities()
    if not cities:
        return make_response(jsonify("Cities Not Found"), 404)
    
    return make_response(jsonify(cities), 200)

@app.route("/showTheatres",methods=["GET"])
def getTheatresForMovie():
    movie = request.args.get("movie")
    city = request.args.get("city")

    if not movie or not city:
        return make_response(jsonify("Please enter both city and movie to view theatres to book"),400)

    theatres = MovieRepository.getTheatresForCityMovie(city, movie)

    if theatres:
        return make_response(jsonify(theatres), 200)
    
    return make_response(jsonify("Sorry, Theatres not found"), 404)


@app.route("/showMovies",methods=["GET"])
def getMoviesForCity():
    city = request.args.get("city")
    if not city:
        return make_respone(jsonify("Please enter a city to view movies"), 400)

    movies = MovieRepository.getAllMoviesForCity(city)

    if not movies:
        return make_response(jsonify("Sorry, Movies not found"), 404)

    return make_response(jsonify(movies), 200)

@app.route("/bookSeats",methods=["POST"])
def bookSeats():
    data = request.get_json()
    movie = data["movie"]
    city = data["city"]

    theatre = data["theatre"]
    noSeats = data["noSeats"]

    if not movie or not city or not noSeats or not theatre:
        return make_response(jsonify("Please enter movie, city, theatre and no of seats to book"), 400)
    
    result = BookingRepository.createBooking(city, movie, theatre, noSeats)
    if not result:
        return make_response(jsonify("Theatre or city used for booking not found"), 400)
    elif result == -1:
        return make_response(jsonify("No of seats requested for booking are not available, reduce the no of seats to book"), 400)
    
    return make_response(jsonify("Tickets booked successfully, Booking ID: "+str(result)), 201)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5050, threaded= True)