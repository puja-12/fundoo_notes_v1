from rest_framework import serializers
from notes.models import Notes


class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = ['title', 'description','user','id']

