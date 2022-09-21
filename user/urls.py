from django.urls import path

from . import views
from .views import  UpdatePassword

urlpatterns = [
    path('register_api/', views.UserRegisterApiView.as_view(),name="register_api"),
    path('log_in/', views.UserLoginApi.as_view(), name="log_in"),
    path('verify/<str:token>',views.VarifyUser.as_view(),name="verify"),
    path('change_password/', UpdatePassword.as_view(), name='change_password'),

]