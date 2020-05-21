from rest_framework import serializers

from establishments.models import Establishment

class EstablishmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Establishment
        fields = (
            'id',
            'name',
            'location'
        )