from rest_framework import serializers

# from labels.models import Labels
from notes.models import Notes


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'description', 'user', 'id','collaborator','is_pinned']
        read_only_fields =['collaborator']



class NoteLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = [ 'labels', 'id']


class ShareNoteSerializer(serializers.ModelSerializer):
    """
    Note Serializer
    """

    class Meta:
        model = Notes
        fields = [ 'id', 'collaborator']


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'is_pinned']
        read_only_fields = ['id', 'title']
