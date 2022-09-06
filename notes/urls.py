from django.urls import path

from . import views
from notes.views import NotesAPIView, LabelAPIView, CollaboratorAPIView

urlpatterns = [
    path('note_api/', NotesAPIView.as_view(),name="note_api"),
    path('delete_api/<int:id>', NotesAPIView.as_view(),name="note_api"),
    # path('note_api/<int:id>', NotesAPIView.as_view(), name="note_api")
    path('label/', LabelAPIView.as_view(), name="label_api"),
    path('collaborator/', CollaboratorAPIView.as_view(), name="collaborator_api")

]
