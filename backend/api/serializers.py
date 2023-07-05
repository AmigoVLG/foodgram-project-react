from rest_framework import serializers

from djoser.serializers import UserSerializer

from .models import User

class CustomUserSerializer(UserSerializer):
    password = serializers.CharField(min_length=8, max_length=150, write_only=True)
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name','password')
        required_fields = ['email']
