from django.urls import path
from .service import UserService

user_service = UserService()

urlpatterns = [    
    path('', user_service.get_user_info, name="user_info"),
    path('login',  user_service.login, name="login"),
    path('logout', user_service.logout, name="logout"),
    path('signup', user_service.signup, name="signup"),
]