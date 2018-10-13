from flask import Flask, render_template, request, jsonify
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
