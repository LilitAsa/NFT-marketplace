# accounts/views_auth_cookie.py
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .serializers_auth import CookieTokenObtainPairSerializer

REFRESH_COOKIE = "refresh_token"
COOKIE_KW = dict(
    httponly=True,
    secure=False,            # True в проде
    samesite="Lax",          # "None" в проде за proxy/https
    path="/",
    max_age=60*60*24*14,
)

class CookieLoginView(TokenObtainPairView):
    serializer_class = CookieTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        if resp.status_code != 200:
            return resp
        refresh = resp.data.pop("refresh", None)  # убираем из body
        if refresh:
            resp.set_cookie("refresh_token", refresh, **COOKIE_KW)
        return resp

class CookieRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data.setdefault("refresh", request.COOKIES.get(REFRESH_COOKIE))
        if not data["refresh"]:
            return Response({"detail": "No refresh cookie"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        payload = dict(serializer.validated_data)

        # НЕ возвращаем refresh в body
        new_refresh = payload.pop("refresh", None)
        resp = Response(payload, status=status.HTTP_200_OK)
        print("DEBUG refresh cookie:", bool(request.COOKIES.get("refresh_token")))


        if new_refresh:
            resp.set_cookie(REFRESH_COOKIE, new_refresh, **COOKIE_KW)
        return resp

class CookieLogoutView(APIView):
    def post(self, request):
        resp = Response({"message": "Logged out"}, status=205)
        resp.delete_cookie(REFRESH_COOKIE, path="/")
        return resp
