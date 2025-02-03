import bcrypt
from uuid import uuid4
from lc.usecase import Usecase
from lc.response import SuccessResponse, FailResponse

from .dto import LoginDTO, JoinDTO
from .entity import User
from .external.database import UserDBPort

class GetUserInformationUsecase(Usecase):

    
    def _run(self):...
        
        
        # JWT authentication

class UserLoginUsecase(Usecase):
    def __init__(self, dto: LoginDTO, user_db_port: UserDBPort):
        super().__init__(dto=dto, db_port=user_db_port)
    
    def _run(self):
        
        
        user: User = self._db_port.get_user_by_username(username=self._dto.username)

        

        if user and bcrypt.checkpw(self._dto.password, user.password):
            return SuccessResponse(data={
                "jwt_token": "abc"
            })
        else:
            return FailResponse(error="Invalid username or password")
        

class UserJoinUsecase(Usecase):
    def __init__(self, dto: JoinDTO, user_db_port: UserDBPort):
        super().__init__(dto=dto, db_port=user_db_port)

    def _run(self):
        #1. Get User by username and email
        user : User = self._db_port.get_user_by_username_email(username=self._dto.username, email=self._dto.email)

        if user:
            return FailResponse(error="Requested user already exists")
        
        #2. bcrypt password with salt
        salt_prefix = uuid4().hex.encode("utf-8")
        hashpw = bcrypt.hashpw(self._dto.password, bcrypt.gensalt(prefix=salt_prefix))
        
               
        self._db_port.add_user(user=User(
            username=self._dto.username,
            password=hashpw,
            email=self._dto.email
        ))

        
        return SuccessResponse()

        