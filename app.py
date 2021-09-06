from flask import Flask, render_template, request
from search import searchPhotos
from recs import homeRecs
import login
import json
from peewee import *
#base de datos
db = SqliteDatabase('people.db')

class Users(Model):
    username = CharField()
    email = CharField()
    password = CharField()
    class Meta:
        database = db 

db.connect()

db.create_tables([Users])


#--------------------------------------------
app = Flask(__name__)

# render login / index
@app.route('/', methods =['GET', 'POST'])
def logIn():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        dbuser = Users.select().where(Users.username == username).get()
        
        if(dbuser.password == password):
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
        NewUser = Users.create(username = username,email = email, password = password)
        NewUser.save()
        return render_template('login.html')
    
    else:
        return render_template('signup.html')

# render index
@app.route('/home')
def home():
  # recs = homeRecs()
  return render_template('index.html')

# render search
@app.route('/search', methods=['POST'])
def search():
  searchTag = request.form["search"]
  loadQ = int(request.form["load"]) * 2
  tags = searchPhotos(searchTag,loadQ)
  return render_template('search.html', searchTag=searchTag, tags=tags)

# funcion para scroll infinito
@app.route('/load')
def load():
  if request.args:
    loadValue = int(request.args.get("value"))  # The 'counter' value sent in the QS
    searchTag = str(request.args.get("tag"))
    tags = searchPhotos(searchTag,loadValue)
    tags = json.dumps(tags)
  return tags

# render profile
@app.route('/profile')
def profile():
  return render_template('profile.html')



if __name__ == "__main__":
  app.run(debug=True)