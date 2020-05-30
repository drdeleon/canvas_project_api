from rest_framework import serializers

from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
        )

    def save(self):
        user = User.objects.create_user(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user