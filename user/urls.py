from django.urls import path

from . import views


urlpatterns = [
    path('register_api/', views.UserRegisterApiView.as_view(),name="register_api"),
    path('log_in/', views.UserLoginApi.as_view(), name="log_in"),
    path('verify/<str:token>',views.VarifyUser.as_view(),name="verify")

]