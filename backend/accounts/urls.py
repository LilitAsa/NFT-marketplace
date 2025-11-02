from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views_auth_cookie import CookieLoginView, CookieRefreshView, CookieLogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CookieLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('logout/', CookieLogoutView.as_view(), name='logout'),
    
    path('me/', MeView.as_view(), name="me"),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/verify/', PasswordResetVerifyView.as_view(), name='password_reset_verify'),
]