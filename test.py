import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  port='3306',
  user="root",
  password="12345678",
  database="boardlab"
  
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE usuarios (  user VARCHAR(255) PRIMARY KEY, email VARCHAR(255),password VARCHAR(255),link VARCHAR(1000))")

# mycursor.execute("CREATE TABLE links (id INT AUTO_INCREMENT PRIMARY KEY,link VARCHAR(700), user VARCHAR(255))")


sql = "SELECT email,password,link FROM usuarios WHERE user ='{}'".format('test3')
mycursor.execute(sql)
myresult = mycursor.fetchall()

print(myresult)
# mycursor.execute("SELECT * FROM usuarios")

# myresult = mycursor.fetchall()
# print(myresult)
# mycursor.execute("SELECT * FROM users")

# myresult = mycursor.fetchall()

# for x in myresult:
#   es.index(index='users', doc_type='people', id=x[0], body={'email':x[1],'password':x[2]})
#signup

# sql = "INSERT INTO users (user, email , password) VALUES (%s, %s)"
# val = (username,email,password)
# mycursor.execute(sql, val)

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")

#sign in

# sql = "SELECT password FROM users WHERE user ={}".format(username)

# mycursor.execute(sql)

# myresult = mycursor.fetchall()

# if myresult[0] == password:        
#     return render_template('index.html', username = username)
# else:
#         return render_template('login.html')


#create link

# sql = "INSERT INTO links (link,user) VALUES (%s, %s)"
# val = (link,username)
# mycursor.execute(sql, val)

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")


#get links

# sql = "SELECT link FROM links WHERE user ={}".format(username)

# mycursor.execute(sql)

# linklist = mycursor.fetchall()

# try:
#   test = es.search(index='table', body={"query": {"match": {'user': username}}})
#   test2 = test['hits']['hits']
#   for i in test2:
#       linklist.append(i['_id'])
#   print (linklist) 

# except:
#   sql = "SELECT link FROM links WHERE user ={}".format(username)
#   mycursor.execute(sql)
#   linklist = mycursor.fetchall()

# link = 'go,hola,adios'  

# link_list= link.split(',')

