from flask import Flask, render_template, request, jsonify, redirect
import json, sys
import sqlite3 as lite

con = None


try:
    con = lite.connect('db/nVanGogh.db')
    
    cur = con.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    
    data = cur.fetchone()
    
    print "SQLite version: %s" % data                
    
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()


app = Flask(__name__, static_url_path='/static')

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@app.route("/login", methods=['POST'])
def login():
    uname = request.form['user']
    pwd = request.form['pass']
    ###TO DO CHECK IF EXISTS IN TABLE AND RETURN USER
    return redirect(redirect_url())

@app.route("/signup", methods=['POST'])
def signup():
    fname = request.form['fname']
    lname = request.form['lname']
    uname = request.form['user2']
    pwd = request.form['pass2']
    address = request.form['address']
    city = request.form['city']
    country = request.form['country']
    ### DO INSERT STATEMENT INTO RTIST TABLE
    return redirect(redirect_url())

@app.route("/artist", methods=['GET','POST'])
def getArtist():
    ##TODO GET THE ARTIST FROM THE DB
    name = request.args.get('name')
    a = {'name':'Marvin Gaye','bio':'Aspiring artist living in Maskachka.','pic':'static/mg.jpeg'}
    artWorks = [] ###todo get all atworks for that artist
    return render_template('artist.html', artist = a, artWorks = artWorks)

@app.route('/')
def index():
	con = lite.connect('db/nVanGogh.db')
   	con.row_factory = lite.Row
      	cur = con.cursor()
   	cur.execute("SELECT ArtTypes.Name FROM ArtTypes") 
   	types = cur.fetchall(); 
	cur.execute("Select ArtWorks.Id, Artists.UserName from ArtWorks INNER JOIN Artists ON ArtWorks.ArtistId == Artists.Id") 
	artWorks = cur.fetchall(); 
	return render_template('index.html', types = types, artWorks = artWorks)

if __name__ == "__main__":
    app.run()
