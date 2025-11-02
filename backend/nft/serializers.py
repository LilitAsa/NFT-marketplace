from rest_framework import serializers
from django.utils import timezone
from .models import *
from accounts.models import User
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class NFTSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = NFT
        fields = [
            'id', 'token_id', 'name', 'description', 'image', 'external_url',
            'owner', 'creator', 'contract_address', 'blockchain', 'token_standard',
            'metadata_url', 'category', 'tags', 'attributes', 'rarity_score',
            'price', 'currency', 'is_listed', 'status', 'views', 'likes_count',
            'is_liked', 'comments_count', 'created_at', 'updated_at', 'minted_at'
        ]
        read_only_fields = ['owner', 'creator', 'created_at', 'updated_at', 'minted_at', 'views']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_comments_count(self, obj):
        return obj.comments.count()

 
class NFTListSerializer(serializers.ModelSerializer):
    """
    Лёгкий сериализатор для списка NFT на странице профиля.
    Возвращает owner/creator как СТРОКИ (username), чтобы избежать вложенных UserSerializer.
    """
    owner = serializers.CharField(source="owner.username", read_only=True)
    creator = serializers.CharField(source="creator.username", read_only=True)
    image_src = serializers.SerializerMethodField()

    class Meta:
        model = NFT
        fields = ["id", "name", "image", "price", "currency", "owner", "creator", "image_src"]
    
    def get_image_src(self, obj):
        request = self.context.get("request")
        if obj.image_file:
            url = obj.image_file.url
            return request.build_absolute_uri(url) if request else url
        if obj.image:
            return obj.image
        # плейсхолдер по умолчанию
        placeholder = settings.MEDIA_URL + "nft_images/placeholder-nft.png"
        return request.build_absolute_uri(placeholder) if request else placeholder


class NFTCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = [
            'token_id', 'name', 'description', 'image', 'external_url',
            'contract_address', 'blockchain', 'token_standard', 'metadata_url',
            'category', 'tags', 'attributes', 'price', 'currency'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        validated_data['creator'] = request.user
        return super().create(validated_data)

class CollectionSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    nfts = NFTSerializer(many=True, read_only=True)
    nfts_count = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Collection
        fields = [
            'id', 'name', 'description', 'banner_image', 'featured_image',
            'owner', 'nfts', 'nfts_count', 'total_volume', 'floor_price',
            'verified', 'is_favorited', 'created_at'
        ]
        read_only_fields = ['owner', 'verified', 'created_at']

    def get_nfts_count(self, obj):
        return obj.nfts.count()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return FavoriteCollection.objects.filter(user=request.user, collection=obj).exists()
        return False

class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['name', 'description', 'banner_image', 'featured_image']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class OwnershipHistorySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    nft = NFTSerializer(read_only=True)
    
    class Meta:
        model = OwnershipHistory
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'nft', 'content', 'timestamp']
        read_only_fields = ['user', 'nft', 'timestamp']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'bidder', 'amount', 'timestamp']
        read_only_fields = ['bidder', 'timestamp']

class BidCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['amount']

class AuctionSerializer(serializers.ModelSerializer):
    nft = NFTSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    highest_bidder = UserSerializer(read_only=True)
    bids = BidSerializer(many=True, read_only=True)
    bids_count = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Auction
        fields = [
            'id', 'nft', 'seller', 'start_price', 'reserve_price', 'current_bid',
            'highest_bidder', 'start_time', 'end_time', 'active', 'bids',
            'bids_count', 'time_remaining', 'created_at'
        ]
        read_only_fields = ['seller', 'created_at']

    def get_bids_count(self, obj):
        return obj.bids.count()

    def get_time_remaining(self, obj):
        if obj.active and obj.end_time > timezone.now():
            return obj.end_time - timezone.now()
        return None

class OfferSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    nft = NFTSerializer(read_only=True)
    
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['buyer', 'created_at']

class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['amount', 'currency', 'expires_at']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    nft = NFTSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'nft', 'timestamp']

class FavoriteCollectionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    collection = CollectionSerializer(read_only=True)
    
    class Meta:
        model = FavoriteCollection
        fields = ['id', 'user', 'collection', 'timestamp']

class NFTStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTStatistics
        fields = '__all__'

class UserStatisticsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserStatistics
        fields = '__all__'