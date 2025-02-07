from abc import abstractmethod
from lc.external.database import DBPort
from ..entity import User

from pymongo import MongoClient
from bson import ObjectId

mongo_client = MongoClient("mongodb://root:root@localhost:27017/")
print("mongo_client", mongo_client)

db = mongo_client["chat_app"]
collections = db["users"]

print(db, collections)
class UserDBPort(DBPort):
    
    @abstractmethod
    def get_user_by_username(self, username:str)->User:
        raise NotImplementedError()
    
    @abstractmethod
    def get_user_by_username_email(self, username:str, email:str)->User:
        raise NotImplementedError()
    
    @abstractmethod
    def add_user(self, user:User):
        raise NotImplementedError()
    
    @abstractmethod
    def get_user_by_id(self, id:str):
        raise NotImplementedError()

class UserDBAdapter(UserDBPort):

    def __init__(self):

        self.collections = collections
    def get_user_by_username(self, username:str)->User:
        
        
        user = self.collections.find_one({"username": username})
        
        print(user)

        if not user: 
            return None

        return User(
            id=user["_id"],
            username=user["username"],
            password=user["password"],
            email=user["email"]
        )
    
    
    def get_user_by_username_email(self, username:str, email:str)->User | None:
        
        result = self.collections.find_one({
            'username': username,
            'email': email
        })
        if not result:
            return None
        return User(id=result["_id"], username=result["username"], password=result["password"], email=result["email"])

    def add_user(self, user:User):
        
        result = self.collections.insert_one( {
            "username": user.username,
            "password": user.password,
            "email": user.email
        })

        print(result)

        
    def get_user_by_id(self, id:str) -> User | None:
        result = self.collections.find_one({"_id": ObjectId(id)})
    
        if not result:
            return None
        
        return User(id=str(result["_id"]), username=result["username"],password="",email=result["email"])

        