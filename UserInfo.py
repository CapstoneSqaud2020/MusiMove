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
    insert = acc.insert_one({"usrnm":username.lower(), "pw":password})
    #returns the account id of the user(which is generated client side when added to the collection)
    return insert.inserted_id


