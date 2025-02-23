from django.urls import path
from .service import UserService
from lc.db import REFRESH_TOKEN, TOKEN_MAP


user_service = UserService(REFRESH_TOKEN, TOKEN_MAP)

urlpatterns = [    
    path('', user_service.get_user_info, name="user_info"),
    path('login',  user_service.login, name="login"),
    path('logout', user_service.logout, name="logout"),
    path('signup', user_service.signup, name="signup"),
    path('token', user_service.token_refresh, name="token_refresh")
]