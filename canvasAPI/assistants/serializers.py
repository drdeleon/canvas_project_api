from rest_framework import serializers

from assistants.models import Assistant

class AssistantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assistant
        fields = (
            'id',
            'name',
            'user',
        )