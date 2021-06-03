from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviesDB.db'
db = SQLAlchemy(app)

engine = create_engine('sqlite:///moviesDB.db',connect_args={'check_same_thread': False})

if __name__ == "__main__":    
    app.run(debug=True)