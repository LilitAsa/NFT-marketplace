from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

REFRESH_COOKIE = "refresh_token"
COOKIE_KW = dict(httponly=True, secure=False, samesite="Lax", path="/", max_age=60*60*24*14)

class CookieLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        refresh = resp.data.pop("refresh", None)
        if refresh:
            resp.set_cookie(REFRESH_COOKIE, refresh, **COOKIE_KW)
        return resp

class CookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data.setdefault("refresh", request.COOKIES.get(REFRESH_COOKIE))
        if not data["refresh"]:
            return Response({"detail": "No refresh cookie"}, status=401)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        resp = Response(serializer.validated_data, status=200)
        if "refresh" in serializer.validated_data:
            resp.set_cookie(REFRESH_COOKIE, serializer.validated_data["refresh"], **COOKIE_KW)
        return resp

class CookieLogoutView(APIView):
    def post(self, request):
        r = request.COOKIES.get(REFRESH_COOKIE)
        if r:
            try: RefreshToken(r).blacklist()
            except Exception: pass
        resp = Response({"message": "Logged out"}, status=205)
        resp.delete_cookie(REFRESH_COOKIE, path="/")
        return resp
