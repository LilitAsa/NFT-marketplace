from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CookieTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # полезно иметь роль и ник прямо в access payload
        token['role'] = user.role
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # НЕ возвращаем refresh (он пойдёт в HttpOnly cookie)
        user = self.user
        data.pop('refresh', None)
        # сразу вернём объект user для фронта
        data['user'] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": getattr(user, "phone", ""),
            "role": user.role,
        }
        return data
