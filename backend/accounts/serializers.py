from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'role', 'date_joined', 'last_login', 'phone'
            ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',"role", 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.filter(username=validated_data['username'])
        if user.exists():
            raise serializers.ValidationError("Username already exists")
        user = User.objects.filter(email=validated_data['email'])
        if user.exists():
            raise serializers.ValidationError("Email already exists")
        
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'collector'),
        )