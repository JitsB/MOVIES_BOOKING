from app import app, db


@app.route('/hello_world', methods=['GET'])
def say_hi():
	return jsonify({"message": "Hello World"})


@app.route('/showCities',methods=['GET'])
def showCities():

    


@app.route('/showTheatres',methods=['GET'])
def getTheatresForMovie():
    movie = request.args.get('movie')
    city = request.args.get('city') # This should come from some saved state as it is passed in previous request
    output_theatres = []

    theatres = CityData[city]
    for theatre in theatres.values():
        for k, v in theatre.items():
            if movie in v['Movies Playing']:
                output_theatres.append(k)
    
    return jsonify({'Theatres to choose from':output_theatres})



@app.route('/showMovies',methods=['GET'])
def getMoviesForCity():
    
    city = request.args.get('city')
    theatres = CityData[city]['Theatres']
    movies_playing = []

    for k,v in theatres.items():
        movies_playing.extend(v['Movies Playing'])
    
    return jsonify({"Movies playing in the city":movies_playing,"message":"Kindly select the movie to watch"})


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5050, threaded= True)