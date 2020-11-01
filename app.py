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
        if session['category'] == "CloudProvider":
            return redirect("/CloudProvider")
        return render_template("/customer/index.html",name=session['name'])
    return redirect("/")

@app.route('/CloudProvider')
def CloudProvider():
    if "name" in session:
        if session['category'] != "CloudProvider":
            return redirect("/dashboard")
        return render_template("/cloud/index.html",name=session['name'],email=session['email'])
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
    category = request.form['category']
    print(name,email,password,category)
    data = {}
    if mongo.Register(email,name,password,category):
        session['email'] = email
        session['name'] = name 
        session['category'] = category

        if category == "CloudProvider":
            data['link'] = '/CloudProvider'
        else:
            data['link'] = '/dashboard' 
        
        data['check'] = True
        
    return data

@app.route('/login_action', methods=['POST'])
def LoginAction():
    email = request.form['email']
    password = request.form['password']
    
    response = {}
    result = mongo.Login(email,password)
    if result['check']:
        
        session['email'] = email
        session['name'] = result['name'] 
        session['category'] = result['category']

        response['check'] = True

        if result['category'] == "CloudProvider":
            response['link'] = '/CloudProvider'
        else:
            response['link'] = '/dashboard' 

    return response


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)