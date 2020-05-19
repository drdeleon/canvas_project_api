from rest_framework import serializers

from assistant.models import Assistant

class AssistantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assistant
        fields = (
            'name'
        )