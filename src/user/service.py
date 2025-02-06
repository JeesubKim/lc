from django.utils.decorators import method_decorator
from django.http import HttpRequest
from lc.response import SuccessResponse, FailResponse
from lc.auth import Authentication, Auth
from .usecase import UserLoginUsecase, UserSignupUsecase, UserRefreshTokenUsecase
from .dto import LoginDTO, SignupDTO, TokenRefreshDTO
from .external.database import UserDBAdapter

# from presentation import UserInfoPresentation
from lc.presentation import Presentation


class UserService:

    def __init__(self, refresh_token_hs=set(), token_map={}):
        self._user_db_adapter = UserDBAdapter()
        self.refresh_token_cache = refresh_token_hs
        self.token_map = token_map
    @method_decorator(Auth())
    def get_user_info(self, request:HttpRequest):
        
        return Presentation.json_response(SuccessResponse())

        # auth_header = request.headers.get("Authorization")
        # if not auth_header:
        #     return Presentation.json_response(FailResponse(error="Authentication error"))
        # else:
        #     return Presentation.json_response(SuccessResponse())
        if request.method == "GET":...
            # login_dto = JoinDTO(request)
            # usecase = GetUserInformationUsecase(dto=login_dto, user_db_port=UserDBAdapter())
            # response = usecase.exec()

            # return Presentation.json_response(response)


    
    def login(self, request:HttpRequest):
        
        if request.method == "POST":
            login_dto = LoginDTO(request)
            usecase = UserLoginUsecase(dto=login_dto, user_db_port=self._user_db_adapter)
            response = usecase.exec()
            if response.success:
                self.token_map[response.data["jwt"]] = response.data["ref"]
                self.token_map[response.data["ref"]] = response.data["jwt"]
                self.refresh_token_cache.add(response.data["ref"])
            return Presentation.json_response(response)

    
    def logout(self, request:HttpRequest):
        if request.method == "GET":
            auth_header = request.headers.get("Authorization")
            access_token = auth_header.split("Bearer ")[1]

            if access_token not in self.token_map: 
                return Presentation.json_response(FailResponse())
            
            ref_token = self.token_map[access_token]
            
            del self.token_map[access_token]
            del self.token_map[ref_token]
            self.refresh_token_cache.remove(ref_token)

            return Presentation.json_response(SuccessResponse())

    
    def signup(self, request:HttpRequest):
        
        if request.method == "POST":
            
            signup_dto = SignupDTO(request)
            usecase = UserSignupUsecase(dto=signup_dto, user_db_port=self._user_db_adapter)
            response = usecase.exec()
            
            
            return Presentation.json_response(response)
    
    @method_decorator(Auth(token_type="refresh"))
    def token_refresh(self, request:HttpRequest):
        if request.method == "POST":
            
            auth_header = request.headers.get("Authorization")
            ref_token = auth_header.split("Bearer ")[1]
            
            if ref_token not in self.refresh_token_cache:
                return Presentation.json_response(FailResponse(error="Invalid Refresh Token"))
            # remove new token
            self.refresh_token_cache.remove(ref_token)
            access_token = self.token_map[ref_token]
            
            del self.token_map[access_token]
            del self.token_map[ref_token]

            token_refresh_dto = TokenRefreshDTO(request)
            usecase = UserRefreshTokenUsecase(dto=token_refresh_dto, user_db_port=self._user_db_adapter)
            response = usecase.exec()

            
            # add new token
            self.token_map[response.data["jwt"]] = response.data["ref"]
            self.token_map[response.data["ref"]] = response.data["jwt"]
            self.refresh_token_cache.add(response.data["ref"])

            return Presentation.json_response(response)
