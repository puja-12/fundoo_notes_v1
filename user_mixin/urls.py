from django.urls import path
from . import views

urlpatterns = [
    path('user_api/', views.UserMixin.as_view()),

]