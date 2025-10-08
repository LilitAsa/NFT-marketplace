from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    image = models.URLField(_('image'), blank=True)
    
    verbose_name = _('Category')
    verbose_name_plural = _('Categories')
    
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
        ('minted', _('Minted')),
        ('listed', _('Listed for Sale')),
        ('auction', _('On Auction')),
        ('sold', _('Sold')),
        ('burned', _('Burned')),
    ]

    token_id = models.CharField(_('Token id'), max_length=100, unique=True)
    name = models.CharField(_('Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    image = models.URLField(_('image'), blank=True)
    external_url = models.URLField(_('external url'), blank=True)
    
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_nfts'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        verbose_name=_('creator'),
        related_name='created_nfts'
    )
    previous_owners = models.ManyToManyField(
        User, 
        through='OwnershipHistory',
        verbose_name=_('previous owners'),
        related_name='previously_owned_nfts',
    )
    
    contract_address = models.CharField(_('contract address'), max_length=42)
    blockchain = models.CharField(_('blockchain'), max_length=20, choices=BLOCKCHAINS, default='Ethereum')
    token_standard = models.CharField(_('token_standard'), max_length=10, choices=NFT_STANDARDS, default='ERC-721')
    metadata_url = models.URLField(_('metadata url'), blank=True)  # IPFS hash
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name=_('category') , null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, verbose_name=_('tags'))
    
    attributes = models.JSONField(_('attributes'), default=dict)  # Traits/metadata
    rarity_score = models.FloatField(_('rarity_score'), null=True, blank=True)
    
    price = models.DecimalField(_('price'), max_digits=20, decimal_places=8, null=True, blank=True)  # Crypto prices
    currency = models.CharField(_('currency'), max_length=10, default='ETH')
    is_listed = models.BooleanField(_('is_listed'), default=False)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='minted')
    
    likes = models.ManyToManyField(User, through='Like', related_name='liked_nfts', blank=True, verbose_name=_('likes'))
    views = models.PositiveIntegerField(_('views'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    minted_at = models.DateTimeField(_('minted at'), auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token_id']),
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['category', 'is_listed']),
        ]
    
    verbose_name = _('NFT')

    def __str__(self):
        return f'{self.name} (#{self.token_id})'

class Tag(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    banner_image = models.URLField(_('banner image'), blank=True)
    featured_image = models.URLField(_('featured image'), blank=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections', verbose_name=_('owner'))
    nfts = models.ManyToManyField(NFT, related_name='collections', blank=True, verbose_name=_('nfts'))
    
    total_volume = models.DecimalField(_('total volume'), max_digits=20, decimal_places=8, default=0)
    floor_price = models.DecimalField(_('floor price'), max_digits=20, decimal_places=8, null=True, blank=True)
    
    verified = models.BooleanField(_('verified'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def __str__(self):
        return self.name

class OwnershipHistory(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, verbose_name=_('nft'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('owner'))
    transaction_hash = models.CharField(_('transaction_hash'), max_length=66)
    price = models.DecimalField(_('price'), max_digits=20, decimal_places=8, null=True, blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = _('Ownership histories')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, verbose_name=_('nft'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'nft']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='comments', verbose_name=_('nft'))
    content = models.TextField(_('content'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

class Auction(models.Model):
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name='auction', verbose_name=_('nft'))
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions', verbose_name=_('seller'))
    
    start_price = models.DecimalField(_('start price'), max_digits=20, decimal_places=8)
    reserve_price = models.DecimalField(_('reserve price'), max_digits=20, decimal_places=8, null=True, blank=True)
    current_bid = models.DecimalField(_('current bid'), max_digits=20, decimal_places=8, null=True, blank=True)
    
    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'))
    
    highest_bidder = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='winning_auctions',
        verbose_name=_('highest bidder')
    )
    
    active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids', verbose_name=_('auction'))
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('bidder'))
    amount = models.DecimalField(_('amount'), max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    
    class Meta:
        ordering = ['-amount']

class Offer(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='offers', verbose_name=_('nft'))
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('buyer'))
    amount = models.DecimalField(_('amount'), max_digits=20, decimal_places=8)
    currency = models.CharField(_('currency'), max_length=10, default='ETH')
    expires_at = models.DateTimeField(_('expires at'), null=True, blank=True)
    status = models.CharField(_('status'), 
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('expired', 'Expired')],
        default='pending'
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

class FavoriteCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_collections', verbose_name=_('user'))
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='favorited_by', verbose_name=_('collection'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'collection']


class NFTStatistics(models.Model):
    nft = models.OneToOneField(NFT, on_delete=models.CASCADE, related_name='stats', verbose_name=_('nft'))
    total_views = models.PositiveIntegerField(_('total views'), default=0)
    total_likes = models.PositiveIntegerField(_('total likes'), default=0)
    total_comments = models.PositiveIntegerField(_('total comments'), default=0)
    last_sale_price = models.DecimalField(_('last_sale price'), max_digits=20, decimal_places=8, null=True, blank=True)
    average_sale_price = models.DecimalField(_('average sale price'), max_digits=20, decimal_places=8, null=True, blank=True)
    
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats', verbose_name=_('user'))
    total_nfts_created = models.PositiveIntegerField(_('total nfts created'), default=0)
    total_nfts_owned = models.PositiveIntegerField(_('total nfts owned'), default=0)
    total_collections = models.PositiveIntegerField(_('total collections'), default=0)
    total_sales = models.DecimalField(_('total sales'), max_digits=20, decimal_places=8, default=0)
    total_volume = models.DecimalField(_('total volume'), max_digits=20, decimal_places=8, default=0)
    
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
