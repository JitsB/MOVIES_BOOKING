from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up the SQLAlchemy Database to be a local file 'desserts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviesDB.db'
db = SQLAlchemy(app)


if __name__ == "__main__":    
    app.run(debug=True)