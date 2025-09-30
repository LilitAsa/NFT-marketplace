from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class NFT(models.Model):
    NFT_STANDARDS = [
        ('ERC-721', 'ERC-721'),
        ('ERC-1155', 'ERC-1155'),
        ('SPL', 'SPL'),  
    ]
    
    BLOCKCHAINS = [
        ('Ethereum', 'Ethereum'),
        ('Polygon', 'Polygon'),
        ('Solana', 'Solana'),
        ('Binance', 'Binance Smart Chain'),
    ]
    
    STATUS_CHOICES = [
        ('minted', 'Minted'),
        ('listed', 'Listed for Sale'),
        ('auction', 'On Auction'),
        ('sold', 'Sold'),
        ('burned', 'Burned'),
    ]

    token_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    external_url = models.URLField(blank=True)
    
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_nfts'
    )
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_nfts'
    )
    previous_owners = models.ManyToManyField(
        User, 
        through='OwnershipHistory',
        related_name='previously_owned_nfts'
    )
    
    contract_address = models.CharField(max_length=42)
    blockchain = models.CharField(max_length=20, choices=BLOCKCHAINS, default='Ethereum')
    token_standard = models.CharField(max_length=10, choices=NFT_STANDARDS, default='ERC-721')
    metadata_url = models.URLField(blank=True)  # IPFS hash
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    
    attributes = models.JSONField(default=dict)  # Traits/metadata
    rarity_score = models.FloatField(null=True, blank=True)
    
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)  # Crypto prices
    currency = models.CharField(max_length=10, default='ETH')
    is_listed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='minted')
    
    likes = models.ManyToManyField(User, through='Like', related_name='liked_nfts', blank=True)
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    minted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token_id']),
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['category', 'is_listed']),
        ]

    def __str__(self):
        return f"{self.name} (#{self.token_id})"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    banner_image = models.URLField(blank=True)
    featured_image = models.URLField(blank=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    nfts = models.ManyToManyField(NFT, related_name='collections', blank=True)
    
    total_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    floor_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OwnershipHistory(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_hash = models.CharField(max_length=66)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Ownership histories'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'nft']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

class Auction(models.Model):
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name='auction')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    
    start_price = models.DecimalField(max_digits=20, decimal_places=8)
    reserve_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    current_bid = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    highest_bidder = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='winning_auctions'
    )
    
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-amount']

class Offer(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='offers')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.CharField(max_length=10, default='ETH')
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('expired', 'Expired')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class FavoriteCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_collections')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'collection']


class NFTStatistics(models.Model):
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name='stats')
    total_views = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    last_sale_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    average_sale_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_nfts_created = models.PositiveIntegerField(default=0)
    total_nfts_owned = models.PositiveIntegerField(default=0)
    total_collections = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    
    updated_at = models.DateTimeField(auto_now=True)


