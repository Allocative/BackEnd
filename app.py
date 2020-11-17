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
        ProjectList = mongo.GetProjectList(session['email'])
        print(ProjectList)
        return render_template("/customer/index.html",name=session['name'],ProjectList=ProjectList)
    return redirect("/")

@app.route('/dashboard/Project/New')
def CustomerNewProject():
    if "name" in session:
        if session['category'] == "CloudProvider":
            return redirect("/CloudProvider")
        CloudList = mongo.GetCloudList()
        print(CloudList)
        return render_template("/customer/CreateProject.html",name=session['name'],CloudList=CloudList)
    return redirect("/")

@app.route('/CloudProvider')
def CloudProvider():
    if "name" in session:
        if session['category'] != "CloudProvider":
            return redirect("/dashboard")
        ProjectList = mongo.GetCloudProject(session['email'])
        return render_template("/cloud/index.html",name=session['name'],email=session['email'],ProjectList=ProjectList)
    return redirect("/")

@app.route('/CloudProvider/AddServer')
def AddServer():
    if "name" in session:
        if session['category'] != "CloudProvider":
            return redirect("/dashboard")
        return render_template("/cloud/serverdetails.html",name=session['name'],email=session['email'])
    return redirect("/")

@app.route('/CloudProvider/ServerDetails')
def ServerDetails():
    if "name" in session:
        if session['category'] != "CloudProvider":
            return redirect("/dashboard")
        return render_template("/cloud/serverdetails.html",name=session['name'],email=session['email'])
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

@app.route('/GetServerAdd',methods=['POST'])
def GetServerAdd():

    ServerLabel = request.form['Label']
    ServerInstances = request.form['Instance']

    ServerRam = request.form['Ram']
    ServerMemory = request.form['Memory']

    LowestTemperature = request.form['LowestTemperature']
    HighestTemperature = request.form['HighestTemperature']
    CurrentTemperature = request.form['CurrentTemperature']

    OptimalLow = request.form['OptimalLow']
    OptimalHigh = request.form['OptimalHigh']

    mongo.AddServer(session['email'],ServerLabel,
    ServerInstances,ServerRam,ServerMemory,
    LowestTemperature,HighestTemperature,CurrentTemperature,
    OptimalLow,OptimalHigh
    )
    print(ServerLabel,ServerInstances,ServerRam,ServerMemory)
    return "asd"

@app.route('/AddProject', methods=['POST'])
def CreateProject():

    Name = request.form['Name']
    Ram = request.form['Ram']
    Memory = request.form['Memory']

    CloudProvider = request.form['CloudProvider']
    StartTime = request.form['StartTime']
    EndTime = request.form['EndTime']    

    print(CloudProvider)
    CloudProviderEmail,CloudProviderName = CloudProvider.split("#")

    mongo.AddProject(Name,Ram,Memory,CloudProviderName,StartTime,EndTime,session['email'],CloudProviderEmail)
    response = {}

    return response




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