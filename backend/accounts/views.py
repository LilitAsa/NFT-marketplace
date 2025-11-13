import requests
import re
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets, mixins, permissions, parsers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import User, UserProfile, PasswordResetToken
from .serializers import *
from .utils.telegram_notifier import send_telegram_message
from .serializers import UserProfileSerializer
from nft.models import NFT
from nft.serializers import NFTListSerializer
from core.pagination import DefaultPageNumberPagination
from accounts.permissions import IsProOrAdmin


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("Пользователь создан")})
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class MeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        request.user.delete()
        return Response({"message": _("Пользователь удален")}, status=204)

    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            if refresh_token is None:
                return Response({"detail": _("Refresh token is required.")},
                                status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()  # заносим в чёрный список
            return Response({"message": _("Вы вышли из системы")}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Проверка старого пароля
            if not self.object.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": [_("Неверный старый пароль")]}, status=400)
            # Установка нового пароля
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            return Response({"message": _("Пароль успешно изменен")})

        return Response(serializer.errors, status=400)
    
    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

class PasswordResetTokenView(APIView):
    permission_classes = [AllowAny]

     # Проверка валидности токена
    def get(self, request, token):
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.is_valid():
                return Response({"message": "Token is valid"}, status=200)
            else:
                return Response({"message": "Token is invalid or expired"}, status=400)
        except PasswordResetToken.DoesNotExist:
            return Response({"message": "Token not found"}, status=404)
        

class PasswordResetRequestView(APIView):
    def post(self, request):
        contact = str(request.data.get('contact')).strip()

        if not contact:
            return Response({"detail": "Введите номер телефона или email."}, status=400)

        user = None
        token_type = None

        # Проверяем email
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(email_pattern, contact):
            try:
                user = User.objects.get(email=contact)
                token_type = 'email'
            except User.DoesNotExist:
                return Response({"detail": "Пользователь с таким email не найден."}, status=404)

        # Проверяем телефон
        else:
            try:
                user = User.objects.get(phone=contact)
                token_type = 'phone'
            except User.DoesNotExist:
                return Response({"detail": "Пользователь с таким телефоном не найден."}, status=404)

        # Удаляем старые токены
        PasswordResetToken.objects.filter(user=user).delete()
        
        # Генерируем короткий токен (6 цифр)
        token = get_random_string(6, allowed_chars='0123456789')

        # Сохраняем токен
        PasswordResetToken.objects.create(user=user, token=token, token_type=token_type)

        # ======== EMAIL ========
        if token_type == 'email':
            reset_link = f"http://127.0.0.1:8000/reset-password/{token}/"
            send_mail(
                subject="Сброс пароля",
                message=f"Перейдите по ссылке для сброса пароля: {reset_link}",
                from_email="noreply@example.com",
                recipient_list=[user.email],
            )

        # ======== PHONE (Telegram + SMS) ========
        else:
            message = f"Ваш код для сброса пароля: {token}"
            print("✅ Отправка сообщения:", message)

            # Отправка в Telegram
            TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
            TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    data={"chat_id": TELEGRAM_CHAT_ID, "text": message}
                )
            except Exception as e:
                print("❌ Ошибка отправки Telegram:", e)

            # Отправка через SMS API (пример для sms.ru)
            try:
                from .utils.sms_sender import send_sms
                send_sms(user.phone, message)
            except Exception as e:
                print("❌ Ошибка отправки SMS:", e)

        return Response(
            {"detail": "Инструкция по сбросу пароля отправлена."},
            status=status.HTTP_200_OK
        )  
    

class PasswordResetConfirmView(APIView):
    def post(self, request, token):
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({"detail": "Неверный токен."}, status=400)

        if not reset_token.is_valid():
            reset_token.delete()
            return Response({"detail": "Токен истёк."}, status=400)

        new_password = request.data.get('new_password')
        if not new_password:
            return Response({"detail": "Введите новый пароль."}, status=400)

        user = reset_token.user
        user.set_password(new_password)
        user.save()

        reset_token.delete()
        return Response({"detail": "Пароль успешно изменён."}, status=200)
    
 
class PasswordResetVerifyView(APIView):
    def post(self, request):
        contact = request.data.get("contact")
        token = request.data.get("token")

        if not contact or not token:
            return Response({"detail": "Введите контакт и токен."}, status=400)

        try:
            user = User.objects.get(email=contact) if '@' in contact else User.objects.get(phone=contact)
            reset_token = PasswordResetToken.objects.filter(user=user, token=token).latest('created_at')
        except (User.DoesNotExist, PasswordResetToken.DoesNotExist):
            return Response({"detail": "Неверный контакт или токен."}, status=400)

        if not reset_token.is_valid():
            reset_token.delete()
            return Response({"detail": "Срок действия токена истёк."}, status=400)

        return Response({"message": "Токен действителен."}, status=200)
    
    
class PasswordResetConfirmView(APIView):
    def post(self, request):
        contact = request.data.get("contact")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not new_password or len(new_password) < 6:
            return Response({"detail": "Пароль слишком короткий."}, status=400)

        try:
            user = User.objects.get(email=contact) if '@' in contact else User.objects.get(phone=contact)
            reset_token = PasswordResetToken.objects.filter(user=user, token=token).latest('created_at')
        except (User.DoesNotExist, PasswordResetToken.DoesNotExist):
            return Response({"detail": "Неверный код или пользователь."}, status=400)

        if not reset_token.is_valid():
            reset_token.delete()
            return Response({"detail": "Срок действия кода истёк."}, status=400)

        user.set_password(new_password)
        user.save()
        reset_token.delete()

        return Response({"message": "Пароль успешно изменён."}, status=200)
    

class UsersViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    /api/users/            -> список пользователей (если нужно)
    /api/users/<username>/ -> профиль (если хочешь возвращать базовые данные)
    /api/users/<username>/nfts?type=owned|created&page=1&page_size=24
    """
    queryset = User.objects.all()
    serializer_class =  UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "username"

    @action(detail=True, methods=["get"], url_path="nfts", permission_classes=[permissions.AllowAny])
    def nfts(self, request, username=None):
        """
        GET /api/users/<username>/nfts?type=owned|created&page=1&page_size=24
        """
        user = get_object_or_404(User, username=username)
        typ = request.query_params.get("type", "owned").lower()

        if typ == "created":
            qs = NFT.objects.filter(creator=user)
        else:
            # по умолчанию owned
            qs = NFT.objects.filter(owner=user)

        # порядок (пример: последние созданные сверху)
        qs = qs.order_by("-id")

        paginator = DefaultPageNumberPagination()
        page = paginator.paginate_queryset(qs, request)
        ser = NFTListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(ser.data)
    

class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # редактировать профиль может только владелец
        return request.method in permissions.SAFE_METHODS or obj.user_id == request.user.id


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = UserProfile.objects.select_related("user")
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    lookup_field = "user__username"   # /api/profile/<username>/

    def get_permissions(self):
        if self.action in ["partial_update", "update", "me", "upload_avatar"]:
            return [permissions.IsAuthenticated(), IsSelfOrReadOnly()]
        return super().get_permissions()

    @action(detail=False, methods=["get"], url_path="me", permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        profile = request.user.profile
        return Response(self.get_serializer(profile).data)

    @action(detail=True, methods=["post"], url_path="avatar")
    def upload_avatar(self, request, **kwargs):
        profile = self.get_object()
        self.check_object_permissions(request, profile)
        file = request.FILES.get("avatar")
        if not file:
            return Response({"detail": "avatar file is required"}, status=400)
        profile.avatar = file
        profile.save(update_fields=["avatar"])
        return Response(self.get_serializer(profile).data)
 

class ProStatsView(APIView):
    permission_classes = [IsAuthenticated, IsProOrAdmin]

    def get(self, request):

        return Response({
            "total_sales": 0,
            "nfts_listed": 0,
            "favourite_chain": "Ethereum",
        })