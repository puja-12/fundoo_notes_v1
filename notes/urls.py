from django.urls import path

from . import views
from notes.views import NotesAPIView, CollaboratorAPIView, PinnedNotes, NoteLabelAPIView

urlpatterns = [
    path('note_api/', NotesAPIView.as_view(),name="note_api"),
    path('delete_api/<int:id>', NotesAPIView.as_view(),name="delete_api"),
    # path('note_api/<int:id>', NotesAPIView.as_view(), name="note_api")
    path('label/', NoteLabelAPIView.as_view(), name="label_api"),
    path('collaborator/', CollaboratorAPIView.as_view(), name="collaborator_api"),
    path('delete_collab/<int:id>', CollaboratorAPIView.as_view(), name="collaborator_api"),
    path('pinned_note/<int:id>', PinnedNotes.as_view(), name="pinned_note")

]
