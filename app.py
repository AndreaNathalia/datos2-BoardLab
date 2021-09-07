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

class Tablero(Model):
    user = ForeignKeyField(Users, backref = 'fotos')
    link = CharField()
    class Meta:
        database = db 

class Holder(Model):
    username = CharField()
    class Meta:
        database = db 
db.connect()

db.create_tables([Users,Tablero,Holder])



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
            return render_template('index.html',username = username)
    
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
  username = request.form['valueuser']
  return render_template('index.html',username = username)

# render search
@app.route('/search', methods=['POST'])
def search():
  username = request.form['searchuser']
  searchTag = request.form["search"]
  loadQ = int(request.form["load"]) * 2
  tags = searchPhotos(searchTag,loadQ)
  return render_template('search.html', searchTag=searchTag, tags=tags,username = username)

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
@app.route('/profile',methods=['POST','GET'])
def profile():
  username = request.form['valueuser']

  linklist = []

  for i in Tablero.select().join(Users).where(Users.username == username):
    linklist.append(i.link)
  print(linklist)

  return render_template('profile.html')

# render profile
@app.route('/adder',methods=['POST','GET'])
def adder():
  link = request.form["link"]
  username = request.form['adderuser']
  dbuser = Users.select().where(Users.username == username).get()
  newlink = Tablero.create(user = dbuser,link= link)
  newlink.save()
  return render_template('profile.html',username = username)


if __name__ == "__main__":
  app.run(debug=True)