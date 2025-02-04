from abc import abstractmethod
from lc.external.database import DBPort
from ..entity import User


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

class UserDBAdapter(UserDBPort):

    def __init__(self):

        self.db = {}
    def get_user_by_username(self, username:str)->User:
        print("get_user_by_username", username)
        user = self.db.get(username, None)
        print(self.db)
        print(user)

        if not user: return None

        return User(
            username=username,
            password=user["password"],
            email=user["email"]
        )
    
    
    def get_user_by_username_email(self, username:str, email:str)->User:
        print(username, email)
        

    def add_user(self, user:User):

        self.db[user.username] = {
            "password": user.password,
            "email": user.email
        }
        
        print(self.db)
        