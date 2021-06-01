from app import app, db
from controller import CityRepository, MovieRepository, TheatreRepository
from flask import Flask, jsonify, request

# To do:
# 1. Change method types to post for some methods ?
# 2. Identify Error handling scenarios ?
# 3. Add status codes to responses

@app.route("/say_hi", methods=["GET"])
def say_hi():
	return jsonify({"message": "Application is running"})

@app.route("/showCities",methods=["GET"])
def showCities():
    # Can show all attributes
    cities = CityRepository.getAllCities()
    if not cities:
        return jsonify({"Message":"Cities not found"})
    
    # for c in cities:

    return jsonify({"Cities":cities})

@app.route("/showTheatres",methods=["GET"])
def getTheatresForMovie():
    movie = request.args.get("movie")
    city = request.args.get("city")

    if not movie or not city:
        return jsonify({"Message":"Please enter both city and movie to view theatres to book"})

    output_theatres = []
    theatres = MovieRepository.getTheatresForCityMovie(city, movie)

    if theatres:
        return jsonify({"Theatres":theatres})
    
    return jsonify("Sorry, Theatres not found")


@app.route("/showMovies",methods=["GET"])
def getMoviesForCity():
    city = request.args.get("city")
    if not city:
        return jsonify({"Message":"Please enter a city to view movies"})

    movies = MovieRepository.getAllMoviesForCity(city)

    if movies:
        return jsonify({"Movies":movies})
    
    return jsonify({"Message":"Sorry, Movies not found"})

@app.route("/bookSeats",methods=["GET"])
def bookSeats():
    movie = request.args.get("movie")
    city = request.args.get("city")

    theatre = request.args.get("theatre")
    noSeats = request.args.get("noSeats")

    if not movie or not city or not noSeats or not theatre:
        return jsonify({"Message":"Please enter movie, city, theatre and no of seats to book"})
    
    result = MovieRepository.bookSeats(city, theatre, movie, noSeats)
    if not result:
        return jsonify({"Message":"Some problem when booking seats"})
    
    return jsonify({"Message":"Tickets booked successfully"})

# Show complete information

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5050, threaded= True)