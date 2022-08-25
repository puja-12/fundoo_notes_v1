from django.urls import path

from . import views
from notes.views import NotesAPIView

urlpatterns = [
    path('note_api/', NotesAPIView.as_view(),name="note_api")
    # path('note_api/<int:id>', NotesAPIView.as_view(), name="note_api")
]
