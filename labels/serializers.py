from rest_framework import serializers
from labels.models import Labels


class LabelSerializer(serializers.ModelSerializer):



    class Meta:
        model = Labels
        fields = ['label','user','id']
        REQUIRED_FIELDS = ['label']


