import bcrypt
import jwt
from datetime import datetime, timedelta

from lc.usecase import Usecase
from lc.response import SuccessResponse, FailResponse
from lc.auth import encode_jwt, Authentication
from .dto import LoginDTO, SignupDTO
from .entity import User
from .external.database import UserDBPort


class GetUserInformationUsecase(Usecase):

    def __init__(self, dto: LoginDTO, user_db_port: UserDBPort):
        super().__init__(dto=dto, db_port=user_db_port)
    
    
    def _run(self):

        return SuccessResponse()
        

        
        # JWT authentication

class UserLoginUsecase(Usecase):
    def __init__(self, dto: LoginDTO, user_db_port: UserDBPort):
        super().__init__(dto=dto, db_port=user_db_port)
    
    def _run(self):
        
        
        user: User = self._db_port.get_user_by_username(username=self._dto.username)



        if user and bcrypt.checkpw(self._dto.password.encode("utf-8"), user.password):
            encoded_jwt = encode_jwt({
                'data': user.username
            })

            return SuccessResponse(data=encoded_jwt)
        else:
            return FailResponse(error="Invalid username or password")
        

class UserSignupUsecase(Usecase):
    def __init__(self, dto: SignupDTO, user_db_port: UserDBPort):
        super().__init__(dto=dto, db_port=user_db_port)

    def _run(self):
        #1. Get User by username and email
        user : User = self._db_port.get_user_by_username_email(username=self._dto.username, email=self._dto.email)

        if user:
            return FailResponse(error="Requested user already exists")
        
        #2. bcrypt password with salt
        hashpw = bcrypt.hashpw(self._dto.password.encode("utf-8"), bcrypt.gensalt())
        
        self._db_port.add_user(user=User(
            username=self._dto.username,
            password=hashpw,
            email=self._dto.email
        ))

        
        return SuccessResponse()

        

