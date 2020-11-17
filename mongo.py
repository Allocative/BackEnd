from passlib.hash import pbkdf2_sha256
import uuid
import pymongo

username = "Allocative"
password = "DeepReinorcementLearningProject"

srv = "mongodb+srv://{}:{}@supplychain-u6nhl.mongodb.net/test?retryWrites=true&w=majority".format(
    username, password)

client = pymongo.MongoClient(srv)

db = client['Allocative']

LoginCollection = db['Auth']
ProjectCollection = db['Project']
ServerCollection = db['Server']

def Register(email,name,password,category):
    q1 = {"email":email}

    result1 = LoginCollection.find(q1)
    check = False

    for  i in  result1:
        if  email == i['email']:
            check = True
            break
    
    if check:
        print("Email Address already exist in database.")
        return False
    else:
        password = pbkdf2_sha256.hash(password)
        q2 = {"name": name, "email": email,
              "password": password,"Id":str(uuid.uuid4()),"category":category}
        
        LoginCollection.insert_one(q2)
        return True

def Login(email,password):
    l1 = {"email": email}
    res = LoginCollection.find(l1)

    data = {}
    data['check'] = False
    for i in res:
        if pbkdf2_sha256.verify(password, i['password']):
            data['name'] = i['name']
            data['category'] = i['category']
            data['check'] = True
    print(data)
    return data

def GetCloudList():
    data = {}
    l1 = {'category':'CloudProvider'}
    result = LoginCollection.find(l1)
    counter = 1 
    for i in result:
        data[counter] = {'name':i['name'],'email':i['email']}
        counter +=1 

    return data

def GetCloudProject(name):
    q1 = {"CloudProviderEmail":name}
    data = {}
    result = ProjectCollection.find(q1)
    counter = 1 
    for i in result:
        data[counter] = {
            "Project":i['Name'],
            "email":i['email'],
            "Ram":i['Ram'],
            "Memory":i['Memory']
                        }
        counter += 1
    return data

def GetProjectList(email):
    q1 = {"email":email}
    data = {}
    result = ProjectCollection.find(q1)
    counter = 1 
    for i in result:
        data[counter] = {
            'Name':i['Name'],
            'Ram':i['Ram'],
            'Memory':i['Memory'],
            'CloudProvider':i['CloudProvider'],
            'StartTime':i['StartTime'],
            'EndTime':i['EndTime']
        }
        counter+=1
    return data 
def AddProject(Name,Ram,Memory,CloudProvider,StartTime,EndTime,email,CloudProviderEmail):
    q1 = {
        'email':email,
        'Name':Name,
        'Ram':Ram,
        'Memory':Memory,
        'CloudProvider':CloudProvider,
        'CloudProviderEmail':CloudProviderEmail,
        'StartTime':StartTime,
        'EndTime':EndTime
    }
    ProjectCollection.insert_one(q1)

def AddServer(userId):
    q1 = {
        "CompanyEmail" : userId,

    }
