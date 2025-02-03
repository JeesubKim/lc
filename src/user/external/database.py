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

class UserDBAdaptor(UserDBPort):

    def get_user_by_username(self, username:str)->User:
        print(username)
    
    
    def get_user_by_username_email(self, username:str, email:str)->User:
        print(username, email)
        