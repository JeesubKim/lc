from django.utils.decorators import method_decorator
from django.http import HttpRequest
from lc.response import SuccessResponse
from lc.auth import Authentication, Auth
from .usecase import UserLoginUsecase, UserSignupUsecase
from .dto import LoginDTO, SignupDTO
from .external.database import UserDBAdapter
# from presentation import UserInfoPresentation
from lc.presentation import Presentation


class UserService:

    def __init__(self):
        self._user_db_adapter = UserDBAdapter()

    
    @method_decorator(Auth)
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
            

            
            return Presentation.json_response(response)

    
    def logout(self, request:HttpRequest):...
        #token expiry

    
    def signup(self, request:HttpRequest):
        
        if request.method == "POST":
            
            signup_dto = SignupDTO(request)
            usecase = UserSignupUsecase(dto=signup_dto, user_db_port=self._user_db_adapter)
            response = usecase.exec()
            
            
            return Presentation.json_response(response)