from flask import Flask, render_template, request, redirect, url_for
from search import searchPhotos
from recs import homeRecs
import mysql.connector 
import flask_profiler
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import json
from peewee import *
import memcache
from elasticsearch.exceptions import ConnectionError as ElasticConnectionError
# Start Kafka Server Vars and clients
topic = "boardlab"
kServer = "localhost:9092"

def jsonserializer(data):
  return json.dumps(data).encode('utf-8')
# Kafka Producer, sends to logstash
producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    value_serializer= jsonserializer# Formatted as JSON
)


# searchs = {
#             'username': request.form['searchuser'],
#             'searchTag': request.form["search"]
#         }


# producer.send(topic, searchs)

mydb = mysql.connector.connect(
  host="localhost",
  port='3306',
  user="root",
  password="12345678",
  database="boardlab"
)

mycursor = mydb.cursor()


#------------------------------------------------
try:
  
  es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
  mycursor.execute("SELECT * FROM users")

  myresult = mycursor.fetchall()

except ElasticConnectionError:
  print("Something is wrong.")
#--------------------------------------------
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
app = Flask(__name__)
app.config["DEBUG"] = True




# You need to declare necessary configuration to initialize
# flask-profiler as follows:
# app.config["flask_profiler"] = {
#     "enabled": app.config["DEBUG"],
#     "storage": {
#         "engine": "sqlite"
#     },
#     "basicAuth":{
#         "enabled": True,
#         "username": "admin",
#         "password": "admin"
#     },
#     "ignore": [
# 	    "^/static/.*"
# 	]
# }




# render login / index


@app.route('/', methods =['GET', 'POST'])
def logIn():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        
        
        try:
          test = es.search(index='users', body={"query": {"match": {'_id': username}}})
          test2 = test['hits']['hits']

          for i in test2:
              userpass = i['_source']['password']
              if userpass == password:
                  userpass2 = userpass
          if userpass2 == password:        
            return render_template('index.html', username = username)
        except ElasticConnectionError:
          sql = "SELECT password FROM users WHERE user ={}".format(username)
          mycursor.execute(sql)
          myresult = mycursor.fetchall()

          if myresult[0] == password:        
            return render_template('index.html', username = username)
            
    else:
        return render_template('login.html')

#render signup
@app.route('/signup', methods =['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        data = {
                    'username' : request.form['username'],
                    'email' : request.form['email'],
                    'password' : request.form['password']
        }


        producer.send('board', data)
        # try:
        #   es.index(index='users', doc_type='people', id=username, body={'email':email,'password':password})
        # except ElasticConnectionError:
        #   print("Something is wrong.")
        # -------------------------------------------------
        # sql = "INSERT INTO users (user, email , password) VALUES (%s, %s,%s)"
        # val = (username,email,password)
        # mycursor.execute(sql, val)
        # mydb.commit()
        # print(mycursor.rowcount, "record inserted.")
        # -------------------------------------------------
        return render_template('login.html')
    
    else:
        return render_template('signup.html')

# render index
@app.route('/home', methods=['GET','POST'])
def home():
  recs = homeRecs()
  username = request.form['homeUser']
  listaBusquedas = busquedasCache(username)
  return render_template('index.html', links=recs, username=username,  searchslist = listaBusquedas)

# render search
@app.route('/search', methods=['GET','POST'])
def search():
  
  username = request.form['searchuser']
  searchTag = request.form["search"]
  loadQ = int(request.form["load"]) * 2
  tags = searchPhotos(searchTag,loadQ)


  # es.index(index='busquedas', doc_type='tag', id=searchTag, body={'username':username})
  mc.set('search',searchTag)
  # listaBusquedas = busquedasCache(username)
  listaBusquedas = ['fut','lentes']

  data = {
            'username': request.form['searchuser'],
            'searchTag': request.form["search"]
        }


  producer.send('board', data)


  return render_template('search.html', searchTag=searchTag, tags=tags, username = username,searchslist = listaBusquedas)

def busquedasCache(username):
  searchslist = []
  if mc.get("searchs") != None:
  
    cache = mc.get("searchs")
    return cache
                                    

  else:
    # test = es.search(index='busquedas', body={"query": {"match": {'username': username}}})
    # test2 = test['hits']['hits']
    # for i in test2:
    #   searchslist.append(i['_id'])
      

  
    # searchslistNoRep = []
    # [searchslistNoRep.append(x) for x in searchslist if x not in searchslistNoRep]
    # SearchsFinal = ' '.join(searchslistNoRep).split()
    SearchsFinal = []
   
    return SearchsFinal


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
@app.route('/profile', methods=['POST','GET'])
def profile():
  username = request.form['profileUser']
  linklist = []
  print(username)
  # for i in Tablero.select().join(Users).where(Users.username == username):
  #   linklist.append(i.link)

  try:
    test = es.search(index='table', body={"query": {"match": {'user': username}}})
    test2 = test['hits']['hits']
    for i in test2:
        linklist.append(i['_id'])
    print (linklist) 

  except ElasticConnectionError:
    linklist_final = []
    sql = "SELECT link FROM links WHERE user ={}".format(username)
    mycursor.execute(sql)
    linklist = mycursor.fetchall() 
    for x in linklist:
      linklist_final.append(x[0]) 
  listaBusquedas = busquedasCache(username)
  return render_template('profile.html', username = username, links = linklist_final, searchslist = listaBusquedas)

# render profile
@app.route('/adder', methods=['POST','GET'])
def adder():
  link = request.form["link"]
  username = request.form['adderUser']
  
  # dbuser = Users.select().where(Users.username == username).get()
  # newlink = Tablero.create(user = dbuser,link= link)
  # newlink.save()
  data = {
            'link': request.form['link'],
            'username': request.form['adderUser']
        }


  producer.send('board', data)
  # try:
  #   es.index(index='table', doc_type='link', id=link, body={'user': username})
  # except ElasticConnectionError:
  #   print("Something is wrong.")
  listaBusquedas = busquedasCache(username)

  sql = "INSERT INTO links (link,user) VALUES (%s, %s)"
  val = (link,username)
  mycursor.execute(sql, val)

  mydb.commit()

  return render_template('profile.html', username = username, searchslist = listaBusquedas)

  #------------------------------------------------


# flask_profiler.init_app(app)

if __name__ == "__main__":
  app.run(debug=True)