from django.urls import path
from .service import UserService

urlpatterns = [    
    path('', UserService.get_user_info, name="user_info"),
    path('login',  UserService.login, name="login"),
    path('logout', UserService.logout, name="logout"),
    path('signup', UserService.signup, name="signup"),
]