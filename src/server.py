from app import app, db
from controller import CityRepository, MovieRepository, TheatreRepository
from flask import Flask, jsonify, request

@app.route("/say_hi", methods=["GET"])
def say_hi():
	return jsonify({"message": "Application is running"})

@app.route("/showCities",methods=["GET"])
def showCities():
    cities = CityRepository.getAllCities()
    return jsonify({"Cities":cities})

@app.route("/showTheatres",methods=["GET"])
def getTheatresForMovie():
    movie = request.args.get("movie")
    city = request.args.get("city")

    if not movie or not city:
        return jsonify({"Message":"Please enter both city and movie to view theatres to book"})

    output_theatres = []
    theatres = TheatreRepository.getTheatresShowingMovie(city, movie)

    if theatres:
        return jsonify({"Theatres":theatres})
    else:
        return jsonify("Sorry, Theatres not found")


@app.route("/showMovies",methods=["GET"])
def getMoviesForCity():
    city = request.args.get("city")
    if not city:
        return jsonify({"Message":"Please enter a city to view movies"})

    movies = MovieRepository.getAllMoviesForCity(city)

    if movies:
        return jsonify({"Movies":movies})
    else:
        return jsonify({"Message":"Sorry, Movies not found"})


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5050, threaded= True)