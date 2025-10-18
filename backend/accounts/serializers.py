from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'role', 'date_joined', 'last_login', 'phone'
            ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'username']
    
    def update(self, instance, validated_data):
        # Обновляем только переданные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password',"role", 'first_name', 'last_name', 'phone']

    def create(self, validated_data):
        user = User.objects.filter(username=validated_data['username'])
        if user.exists():
            raise serializers.ValidationError(_("Username already exists"))
        user = User.objects.filter(email=validated_data['email'])
        if user.exists():
            raise serializers.ValidationError(_("Email already exists"))
        
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'collector'),
            phone=validated_data.get('phone', ''),
            telegram_chat_id=validated_data.get('telegramChatId', '')
        )

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                _("Пароль слишком короткий (Password too short)")
            )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Неверный старый пароль")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
