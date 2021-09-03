from flask import Flask, render_template, request
from search import searchPhotos
from recs import homeRecs
import login
import json

app = Flask(__name__)

# render login / index
@app.route('/', methods =['GET', 'POST'])
def logIn():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        if(login.dbUsuarios['username'] == username and login.dbUsuarios['password'] == password):
            print(login.dbUsuarios)
            return render_template('index.html')
    
    else:
        return render_template('login.html')

#render signup
@app.route('/signup', methods =['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        login.signup(username, email, password)
        return render_template('login.html')
    
    else:
        return render_template('signup.html')

@app.route('/home')
def searchS():
  # recs = homeRecs()
  return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
  searchTag = request.form["search"]
  loadQ = int(request.form["load"]) * 2
  tags = searchPhotos(searchTag,loadQ)
  return render_template('search.html', searchTag=searchTag, tags=tags)

@app.route('/load')
def load():
  if request.args:
    loadValue = int(request.args.get("value"))  # The 'counter' value sent in the QS
    searchTag = str(request.args.get("tag"))
    tags = searchPhotos(searchTag,loadValue)
    tags = json.dumps(tags)
  return tags



if __name__ == "__main__":
  app.run(debug=True)