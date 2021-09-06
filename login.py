from peewee import *

#dicccionario para simular la base de datos
dbUsuarios = {"username": "", "email": "", "password": ""}

#Funcion para registrar un nuevo usuario
def signup(username, email, password):
    dbUsuarios["username"] = username
    dbUsuarios["email"] = email
    dbUsuarios["password"] = password

    print(dbUsuarios)


#Funcion para ingresar a home
def login(username, password):
    if(dbUsuarios['username'] == username and dbUsuarios['password'] == password):
        pass
    

