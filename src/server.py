from flask import Flask, jsonify, request

app = Flask(__name__)


CityData = {
        'Mumbai':{
            'Theatres':{
               'Ashok Anil Multiplex': 
                {
                    'Movies Playing':['Shawshank Redemption','ABCD'],
                    'Seats':60,
                    'Booked':0
                },
                'Sapna Theatres':
                {
                    'Movies Playing':['Fight Club','ABCD 2'],
                    'Seats':60,
                    'Booked':0
                }
            }
        },
        'Bangalore':{
            'Theatres':{
                'PVR-Kormangala': 
                {
                    'Movies Playing':['Shawshank Redemption','Inception'],
                    'Seats':60,
                    'Booked':0
                },
                'PVR-whitefiled':
                {
                    'Movies Playing':['Fight Club','3 Idiots','Inception'],
                    'Seats':60,
                    'Booked':0
                }
            }
        }
    }

@app.route('/hello_world', methods=['GET'])
def say_hi():
	return jsonify({"message": "Hello World"})

@app.route('/', methods=['GET'])
def index():
    cities = ['Mumbai','Bangalore','Delhi','Kolkata','Hyderabad']
    return jsonify({"message":"Welcome to movies booking system, Kindly select a city from the list to proceed",
                    "Cities":cities})


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