from flask import Flask, render_template, request, jsonify, redirect, url_for, session
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

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           '/'


@app.route("/loginDemo", methods=['POST'])
def loginDemo():
    uname = request.form['user']
    pwd = request.form['pass']
    con = lite.connect('db/nVanGogh.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Customer Where Customer.UserName == ?", [uname]) 
    user = cur.fetchall()
    print(user)
    if len(user) and user[0]['Password'] == pwd:
    	session['loggedIn'] = True
    	session['level'] = user[0]['Level']
    	return redirect(redirect_url())
    else:
    	return redirect("/")   

@app.route("/login", methods=['POST'])
def login():
    uname = request.form['user']
    pwd = request.form['pass']
    con = lite.connect('db/nVanGogh.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Artists Where Artists.UserName == ?", [uname]) 
    user = cur.fetchall()
    if len(user) and user[0]['Password'] == pwd:
	    return redirect(url_for("getProfile", name = uname))
    else:
	    return redirect("/")   

@app.route("/logout")
def logout():
	session.clear()
	return redirect(redirect_url())

@app.route("/profile/<name>")
def getProfile(name):
       
    con = lite.connect('db/nVanGogh.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Artists Where Artists.UserName == ?", [name]) 
    a = cur.fetchall()

    if len(a): 
	    cur.execute("SELECT * FROM Artists Where Artists.UserName == ?", [name]) 
	    artWorks = cur.fetchall()
	    return render_template('profile.html', artist = a, artWorks = artWorks)
    else:
    	    return redirect("/")  

    
@app.route("/signup", methods=['POST'])
def signup():
    fname = request.form['fname']
    lname = request.form['lname']
    uname = request.form['user2']
    pwd = request.form['pass2']
    address = request.form['address']
    city = request.form['city']
    country = request.form['country']

    con = lite.connect('db/nVanGogh.db')
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("INSERT Artists.Password FROM Artists Where Artists.UserName == ?", [uname]) 	

    return redirect(redirect_url())

@app.route("/artist/<name>")
def getArtist(name):
	con = lite.connect('db/nVanGogh.db')
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM Artists Where Artists.UserName == ?", [name])
	a = cur.fetchall()
	cur.execute("Select ArtWorks.Id, ArtWorks.Description, ArtWorks.Item, ArtWorks.Name from ArtWorks INNER JOIN Artists ON ArtWorks.ArtistId == Artists.Id where Artists.UserName == ?", [name]) 
	artWorks = cur.fetchall()
	return render_template('artist.html', artist = a, artWorks = artWorks)


@app.route("/allArtists")
@app.route('/allArtists/<uname>')
def getAllArtists(uname=None):
	con = lite.connect('db/nVanGogh.db')
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM Artists order by id")
	artists = cur.fetchall()
	artMen = None
    	if uname: 
	    cur.execute("SELECT * FROM Artists where Artists.UserName == ?", [uname])
	    artMen = cur.fetchall()

	return render_template('allArtists.html', allArtists=artists, uname = uname, artMen = artMen)

@app.route("/about")
def about():
	return render_template('about.html')


@app.route('/')
@app.route('/<typ>')
def index(typ=None):

	
	con = lite.connect('db/nVanGogh.db')
   	con.row_factory = lite.Row
      	cur = con.cursor()
	cur.execute("SELECT * FROM ArtTypes") 
   	types = cur.fetchall(); 
	if typ :
		cur.execute("Select ArtWorks.Id, Artists.UserName, Artists.FirstName, Artists.LastName, ArtWorks.Description, ArtWorks.Item, ArtWorks.Name from ArtWorks INNER JOIN Artists ON ArtWorks.ArtistId == Artists.Id where ArtWorks.ArtTypeId == ?", typ) 
			
	else:
		cur.execute("Select Artists.UserName, Artists.FirstName, Artists.LastName, ArtWorks.Description, ArtWorks.Item, ArtWorks.Name from ArtWorks INNER JOIN Artists ON ArtWorks.ArtistId == Artists.Id") 
	artWorks = cur.fetchall(); 
	print(types)
	return render_template('index.html', types = types, artWorks = artWorks)

if __name__ == "__main__":
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run()
