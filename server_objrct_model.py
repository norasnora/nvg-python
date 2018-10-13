from flask import Flask, render_template, request, jsonify
import json, sys, os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


con = None


try:
	project_dir = os.path.dirname(os.path.abspath(__file__))
	database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/nVanGogh.db"))

	app = Flask(__name__, static_url_path='/static')
	app.config["SQLALCHEMY_DATABASE_URI"] = database_file
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db = SQLAlchemy(app)	            
    
except IntegrityError as e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources
some_engine = create_engine(database_file)

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()

# work with sess





class ArtTypes(Base):
	__tablename__ = 'ArtWorks'
 	__table_args__ = {'extend_existing': True} 
    	Id =  db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    	Type = db.Column(db.String(80), unique=True, nullable=False)

    	def __repr__(self):
        	return "<Id: {}>".format(self.Id)

class ArtWorks(Base):
    	__tablename__ = 'ArtWorks'
	__table_args__ = {'extend_existing': True} 	
	Id =  db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	ArtistId = db.Column(db.Integer, nullable=False)
	ArtTypeId = db.Column(db.Integer, nullable=False)
	Name = db.Column(db.String(80), nullable=False)
	Description = db.Column(db.String(20000))
	Item = db.Column(db.String(80))
	
	def __repr__(self):
        	return "<Id: {}>".format(self.Id)




@app.route('/')
def index():
	types = ArtTypes.query.all()
	artWorks = ArtWorks.query.all()
	return render_template('index.html', types = types, artWorks = artWorks)

if __name__ == "__main__":
    app.run()
