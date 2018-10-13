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

@app.route("/")
def index():
    page_name = "index"
    return render_template('%s.html' % page_name)
 
if __name__ == "__main__":
    app.run()
