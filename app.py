from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_url_path='/static')

app.debug = True 
app.secret_key = "NothingIsSecret"


@app.route('/')
def HomePage():
   return render_template("index.html")

@app.route('/login')
def LoginPage():
   return render_template("login.html")


# Ajax Call Functions 

@app.route('/sign_action', methods=['POST'])
def RegisterUser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
   
    print(name,email,password)
    return "Post Request Works"

@app.route('/login_action', methods=['POST'])
def LoginAction():
    email = request.form['email']
    password = request.form['password']
    print(email, password)

    return "Login Post Works"


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)