from django.urls import path
from labels.views import LabelAPIView


urlpatterns = [
    path('create_label/', LabelAPIView.as_view(), name="Create_label"),
    path('get_label/', LabelAPIView.as_view(), name="Get_label"),
    path('delete_label/<int:id>/', LabelAPIView.as_view(), name="delete_label"),

]