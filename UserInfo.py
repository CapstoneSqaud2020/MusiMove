#yall need to istall this package to connect to mongo
import pymongo
#connects to mongodb if you don't see the pw in the google docs pls message Jenn
client = pymongo.MongoClient("mongodb+srv://CapstoneCrew:Rutgers2020@cluster0-lvmuw.azure.mongodb.net/test?retryWrites=true&w=majority")
#connects to project db
db = client.MusiMove

#check that the user exists returns a boolean
def userExists(username):
    acc = db.account#connects to the specific collection in the db, in this case it connects to the collection accounts
    if(acc.count_documents({"usrnm":username.lower()})>0):
        return 1
    else:
        return 0 
#checks username pw matches 
def login(username, password):
    acc = db.account
    user = acc.find({"usrnm":username.lower(), "pw":password})
    #return user's account id if user exists else returns 0
    if (user.count()>0):
        return user[0].get("_id")
    else:
        return 0
#adds username&pw to db
def addNewUser(username, password):
    acc = db.account
    id = 100000004 + inc()
    insert = acc.insert_one({"_id":id, "usrnm":username.lower(), "pw":password, "timeout": "Stay On", "musicOpt":"Radio", "radStation": 0})
    #returns the account id of the user(which is generated client side when added to the collection)
    return id

def inc():
    c = db.count
    num = c.find({"_id":'5e60a40c1c9d4400002379d4'})
    c.update_one({"_id":'5e60a40c1c9d4400002379d4'}, {"$inc": {"count": 1}})
    return num[0].get("count")

def deleteUser(user_id):
    acc = db.account
    acc.delete_one({"_id":user_id})

def updateStopTime(user_id, value):
    acc = db.account
    acc.update_one({"_id":user_id}, {"$set": {"timeout": value}})

def getStopTime(user_id):
    acc = db.account
    user = acc.find({"_id":user_id})
    return user[0].get("timeout")

def updateMusicOpt(user_id, value):
    acc = db.account
    acc.update_one({"_id":user_id}, {"$set": {"musicOpt": value}})

def getMusicOpt(user_id):
    acc = db.account
    user = acc.find({"_id":user_id})
    return user[0].get("musicOpt")


def updateRadioStation(user_id, value):
    acc = db.account
    acc.update_one({"_id":user_id}, {"$set": {"radStation": value}})

def getRadioStation(user_id):
    acc = db.account
    user = acc.find({"_id":user_id})
    return user[0].get("radStation")