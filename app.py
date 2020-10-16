from flask import Flask, render_template, request, redirect, url_for, session
import mongo

app = Flask(__name__, static_url_path='/static')

app.debug = True 
app.secret_key = "NothingIsSecret"


@app.route('/')
def HomePage():
    if "name" in session: 
        return redirect("/dashboard")
    return render_template("index.html")

@app.route('/login')
def LoginPage():
    if "name" in session: 
        return redirect("/dashboard")
    return render_template("login.html")

@app.route('/dashboard')
def DashBoard():
    if "name" in session:
        return "DashBoard"
    return redirect("/")
    

@app.route('/logout')
def LogOut():
    session.clear()
    return redirect("/")

# Ajax Call Functions 

@app.route('/sign_action', methods=['POST'])
def RegisterUser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
   
    print(name,email,password)
    data = {}
    if mongo.Register(email,name,password):
        session['email'] = email
        session['name'] = name 
        data['check'] = True
        data['link'] = '/dashboard'

    return data

@app.route('/login_action', methods=['POST'])
def LoginAction():
    email = request.form['email']
    password = request.form['password']
    print(email, password)

    response = {}
    result = mongo.Login(email,password)
    if response['check']:
        session['email'] = email
        session['name'] = result['name'] 
        response['check'] = True
        response['link'] = '/dashboard'

    return response


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)