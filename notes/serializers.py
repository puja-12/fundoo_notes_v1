from rest_framework import serializers

from labels.models import Labels
from notes.models import Notes


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description', 'user', 'id']


class NoteLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = [ 'user','labels', 'id']


class ShareNoteSerializer(serializers.ModelSerializer):
    """
    Note Serializer
    """

    class Meta:
        model = Notes
        fields = [ 'user','id', 'collaborator']
