from flask import Flask, render_template, request
import login

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



if __name__ == "__main__":
  app.run(debug=True)