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


@app.route("/")
def index():
    page_name = "index"
    return render_template('%s.html' % page_name)

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


if __name__ == "__main__":
    app.run()
