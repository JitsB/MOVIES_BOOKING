from app import app, db
from controller import CityRepository, MovieRepository, TheatreRepository, BookingRepository
from flask import Flask, jsonify, request

# To do:

# 2. Identify Error handling scenarios ?


@app.route("/say_hi", methods=["GET"])
def say_hi():
	return jsonify({"message": "Application is running"},status=200)

@app.route("/showCities",methods=["GET"])
def showCities():
    
    cities = CityRepository.getAllCities()
    if not cities:
        return jsonify({"Message":"Cities not found"},status=404)

    return jsonify({"Cities":cities},status=200)

@app.route("/showTheatres",methods=["GET"])
def getTheatresForMovie():
    movie = request.args.get("movie")
    city = request.args.get("city")

    if not movie or not city:
        return jsonify({"Message":"Please enter both city and movie to view theatres to book"},status=400)

    output_theatres = []
    theatres = MovieRepository.getTheatresForCityMovie(city, movie)

    if theatres:
        return jsonify({"Theatres":theatres},status=200)
    
    return jsonify("Sorry, Theatres not found",status=404)


@app.route("/showMovies",methods=["GET"])
def getMoviesForCity():
    city = request.args.get("city")
    if not city:
        return jsonify({"Message":"Please enter a city to view movies"},status=400)

    movies = MovieRepository.getAllMoviesForCity(city)

    if movies:
        return jsonify({"Movies":movies},statu=200)
    
    return jsonify({"Message":"Sorry, Movies not found"},status=404)

@app.route("/bookSeats",methods=["POST"])
def bookSeats():
    data = request.get_json()
    movie = data["movie"]
    city = data["city"]

    theatre = data["theatre"]
    noSeats = data["noSeats"]

    if not movie or not city or not noSeats or not theatre:
        return jsonify({"Message":"Please enter movie, city, theatre and no of seats to book"},status=400)
    
    result = BookingRepository.createBooking(city, movie, theatre, noSeats)
    if not result:
        return jsonify({"Message":"Some problem when booking seats"},status=) # ?
    elif result == -1:
        return jsonify({"Message":"No of seats requested for booking are not available, reduce the no of seats to book"},status=400)
    
    return jsonify({"Message":"Tickets booked successfully"}, status=201)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5050, threaded= True)