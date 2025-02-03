from django.http import HttpRequest, JsonResponse

from .usecase import GetUserInformationUsecase, UserLoginUsecase
from .dto import LoginDTO, JoinDTO
from .external.database import UserDBAdaptor
# from presentation import UserInfoPresentation
from lc.presentation import Presentation


class UserService:


    @staticmethod
    def get_user_info(request:HttpRequest):
        if request.method == "GET":
            login_dto = JoinDTO(request)
            usecase = GetUserInformationUsecase(dto=login_dto, user_db_port=UserDBAdaptor())
            response = usecase.exec()

            return Presentation.json_response(response)


    @staticmethod
    def login(request:HttpRequest):
        
        if request.method == "POST":
            login_dto = LoginDTO(request)
            usecase = UserLoginUsecase(dto=login_dto, user_db_port=UserDBAdaptor())
            response = usecase.exec()
            
            
            return Presentation.json_response(response)

    @staticmethod
    def logout(request:HttpRequest):...

    @staticmethod
    def signup(request:HttpRequest):...