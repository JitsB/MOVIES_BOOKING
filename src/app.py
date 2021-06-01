from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Set up the SQLAlchemy Database to be a local file 'desserts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviesDB.db'
db = SQLAlchemy(app)

# an Engine, which the Session will use for connection
# resources
engine = create_engine('sqlite:///moviesDB.db',connect_args={'check_same_thread': False})

# # create a configured "Session" class
# Session = sessionmaker(bind=some_engine)

# # create a Session
# session = Session()

if __name__ == "__main__":    
    app.run(debug=True)