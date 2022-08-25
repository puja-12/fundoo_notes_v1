from django.urls import path

from . import views
from user.views import  UserRegisterApiView,UserLoginApi

urlpatterns = [
    path('register_api/', UserRegisterApiView.as_view(),name="register_api"),
    path('log_in/', UserLoginApi.as_view(), name="log_in")

]