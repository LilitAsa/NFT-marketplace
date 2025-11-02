from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns 
from django.views.i18n import set_language
from rest_framework.routers import DefaultRouter
from accounts.views import ProfileViewSet, UsersViewSet


router = DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r'users', UsersViewSet, basename='user')

urlpatterns = [
    path('rosetta/', include('rosetta.urls')),
    path('set_language/', set_language, name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/accounts/', include('accounts.urls')),
    path('api/nft/', include('nft.urls')),
    path("api/", include(router.urls)),          # /api/users/<username>/nfts
    path("api/auth/", include("accounts.urls")), # твои register/login/me/... из accounts/urls.py
    # path('api/users/<str:username>/nfts/', UserNFTsView.as_view(), name='user-nfts'),
] + debug_toolbar_urls()

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
