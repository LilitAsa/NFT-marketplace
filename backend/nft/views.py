# nft/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from .filters import NFTFilter


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # your user serializer
    lookup_field = 'username'
    lookup_value_regex = r'[\w.@+-]+'

    @action(detail=True, methods=['get'], url_path='nfts', permission_classes=[AllowAny])
    def nfts(self, request, username=None):
        user = self.get_object()
        nft_type = request.query_params.get('type', 'owned')

        qs = NFT.objects.select_related('owner', 'creator', 'category') \
                        .prefetch_related('tags', 'likes', 'comments')

        if nft_type == 'owned':
            qs = qs.filter(owner=user)
        elif nft_type == 'created':
            qs = qs.filter(creator=user)
        else:
            qs = qs.filter(owner=user)

        paginator = UserNFTsPagination()
        page = paginator.paginate_queryset(qs.order_by('-created_at'), request)
        ser = NFTSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(ser.data)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class NFTViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = NFT.objects.select_related('owner', 'creator', 'category').prefetch_related('tags', 'likes', 'comments')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NFTFilter
    search_fields = ['name', 'description', 'token_id']
    ordering_fields = ['created_at', 'price', 'views', 'rarity_score']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return NFTCreateSerializer
        return NFTSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, creator=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        nft = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, nft=nft)
        
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def list_for_sale(self, request, pk=None):
        nft = self.get_object()
        if nft.owner != request.user:
            return Response({'error': _('Only owner can list for sale')}, status=status.HTTP_403_FORBIDDEN)
        
        price = request.data.get('price')
        if not price:
            return Response({'error': _('Price is required')}, status=status.HTTP_400_BAD_REQUEST)
        
        nft.price = price
        nft.is_listed = True
        nft.status = 'listed'
        nft.save()
        
        return Response({'status': _('NFT listed for sale')})

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        nft = self.get_object()
        if nft.owner != request.user:
            return Response({'error': _('Only owner can transfer NFT')}, status=status.HTTP_403_FORBIDDEN)
        
        new_owner_username = request.data.get('new_owner')
        if not new_owner_username:
            return Response({'error': _('New owner username is required')}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_owner = User.objects.get(username=new_owner_username)
        except User.DoesNotExist:
            return Response({'error': _('User not found')}, status=status.HTTP_404_NOT_FOUND)
        
        OwnershipHistory.objects.create(
            nft=nft,
            owner=new_owner,
            transaction_hash=request.data.get('transaction_hash', ''),
            price=nft.price
        )
        
        nft.owner = new_owner
        nft.is_listed = False
        nft.status = 'minted'
        nft.save()
        
        return Response({'status': _('NFT transferred successfully')})

    @action(detail=True, methods=['get'])
    def ownership_history(self, request, pk=None):
        nft = self.get_object()
        history = OwnershipHistory.objects.filter(nft=nft).select_related('owner').order_by('-timestamp')
        serializer = OwnershipHistorySerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        nft = self.get_object()
        comments = Comment.objects.filter(nft=nft).select_related('user').order_by('-timestamp')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        nft = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, nft=nft)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Collection.objects.select_related('owner').prefetch_related('nfts')
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'total_volume', 'floor_price']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionCreateSerializer
        return CollectionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_nft(self, request, pk=None):
        collection = self.get_object()
        if collection.owner != request.user:
            return Response({'error': _('Only collection owner can add NFTs')}, status=status.HTTP_403_FORBIDDEN)
        
        nft_id = request.data.get('nft_id')
        if not nft_id:
            return Response({'error': _('nft_id is required')}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nft = NFT.objects.get(id=nft_id, owner=request.user)
        except NFT.DoesNotExist:
            return Response({'error': _('NFT not found or you are not the owner')}, status=status.HTTP_404_NOT_FOUND)
        
        collection.nfts.add(nft)
        return Response({'status': _('NFT added to collection')})

    @action(detail=True, methods=['post'])
    def remove_nft(self, request, pk=None):
        collection = self.get_object()
        if collection.owner != request.user:
            return Response({'error': _('Only collection owner can remove NFTs')}, status=status.HTTP_403_FORBIDDEN)
        
        nft_id = request.data.get('nft_id')
        if not nft_id:
            return Response({'error': _('nft_id is required')}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nft = NFT.objects.get(id=nft_id)
        except NFT.DoesNotExist:
            return Response({'error': _('NFT not found')}, status=status.HTTP_404_NOT_FOUND)
        
        collection.nfts.remove(nft)
        return Response({'status': _('NFT removed from collection')})

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        collection = self.get_object()
        favorite, created = FavoriteCollection.objects.get_or_create(
            user=request.user, 
            collection=collection
        )
        
        if not created:
            favorite.delete()
            return Response({'status': 'removed from favorites'})
        return Response({'status': 'added to favorites'})

class AuctionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Auction.objects.select_related('nft', 'seller', 'highest_bidder').prefetch_related('bids')
    serializer_class = AuctionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['active', 'seller']
    ordering_fields = ['start_time', 'end_time', 'current_bid']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('include_ended') != 'true':
            queryset = queryset.filter(active=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=True, methods=['post'])
    def place_bid(self, request, pk=None):
        auction = self.get_object()
        
        if not auction.active:
            return Response({'error': _('Auction has ended')}, status=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() > auction.end_time:
            auction.active = False
            auction.save()
            return Response({'error': _('Auction has ended')}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': _('Bid amount is required')}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return Response({'error': _('Invalid bid amount')}, status=status.HTTP_400_BAD_REQUEST)
        
        if auction.current_bid and amount <= auction.current_bid:
            return Response({'error': _('Bid must be higher than current bid')}, status=status.HTTP_400_BAD_REQUEST)
        
        if amount < auction.start_price:
            return Response({'error': _('Bid must be at least the start price')}, status=status.HTTP_400_BAD_REQUEST)
        
        bid = Bid.objects.create(
            auction=auction,
            bidder=request.user,
            amount=amount
        )
        
        auction.current_bid = amount
        auction.highest_bidder = request.user
        auction.save()
        
        return Response({'status': _('Bid placed successfully')})

    @action(detail=True, methods=['post'])
    def end_auction(self, request, pk=None):
        auction = self.get_object()
        
        if auction.seller != request.user:
            return Response({'error': _('Only the seller can end the auction')}, status=status.HTTP_403_FORBIDDEN)
        
        auction.active = False
        auction.save()
        
        if auction.highest_bidder:
            auction.nft.owner = auction.highest_bidder
            auction.nft.is_listed = False
            auction.nft.status = 'sold'
            auction.nft.save()
            
            OwnershipHistory.objects.create(
                nft=auction.nft,
                owner=auction.highest_bidder,
                transaction_hash=f"auction_{auction.id}",
                price=auction.current_bid
            )
        
        return Response({'status': _('Auction ended successfully')})

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.select_related('user', 'nft')
    ordering = ['-timestamp']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        nft_id = self.request.data.get('nft_id')
        try:
            nft = NFT.objects.get(id=nft_id)
        except NFT.DoesNotExist:
            return Response({'error': _('NFT not found')}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(user=self.request.user, nft=nft)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

class OfferViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Offer.objects.select_related('buyer', 'nft')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OfferCreateSerializer
        return OfferSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('my_offers') == 'true':
            queryset = queryset.filter(buyer=self.request.user)
        elif self.request.query_params.get('received_offers') == 'true':
            queryset = queryset.filter(nft__owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        nft_id = self.request.data.get('nft_id')
        try:
            nft = NFT.objects.get(id=nft_id)
        except NFT.DoesNotExist:
            return Response({'error': _('NFT not found')}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(buyer=self.request.user, nft=nft)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        offer = self.get_object()
        
        if offer.nft.owner != request.user:
            return Response({'error': _('Only NFT owner can accept offers')}, status=status.HTTP_403_FORBIDDEN)
        
        if offer.status != 'pending':
            return Response({'error': _('Offer is not pending')}, status=status.HTTP_400_BAD_REQUEST)
        
        offer.nft.owner = offer.buyer
        offer.nft.is_listed = False
        offer.nft.status = 'sold'
        offer.nft.price = offer.amount
        offer.nft.save()
        
        OwnershipHistory.objects.create(
            nft=offer.nft,
            owner=offer.buyer,
            transaction_hash=f"offer_{offer.id}",
            price=offer.amount
        )
        
        offer.status = 'accepted'
        offer.save()
        
        Offer.objects.filter(nft=offer.nft, status='pending').update(status='rejected')
        
        return Response({'status': 'Offer accepted'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        offer = self.get_object()
        
        if offer.nft.owner != request.user:
            return Response({'error': _('Only NFT owner can reject offers')}, status=status.HTTP_403_FORBIDDEN)
        
        offer.status = 'rejected'
        offer.save()
        return Response({'status': 'Offer rejected'})
