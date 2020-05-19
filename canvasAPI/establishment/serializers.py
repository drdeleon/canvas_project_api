from rest_framework import serializers

from establishment.model import Establishment

class EstablishmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Establishment
        fields( 
            'name',
            'location'
        )