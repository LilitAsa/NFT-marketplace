from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'nfts', views.NFTViewSet, basename='nft')
router.register(r'collections', views.CollectionViewSet, basename='collection')
router.register(r'auctions', views.AuctionViewSet, basename='auction')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'offers', views.OfferViewSet, basename='offer')

urlpatterns = [
    path('', include(router.urls)),
]