from django.contrib import admin
from .models import *

class OwnershipHistoryInline(admin.TabularInline):
    model = OwnershipHistory
    extra = 0
    readonly_fields = ['timestamp']

@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ['name', 'token_id', 'owner', 'creator', 'status', 'is_listed', 'price', 'created_at']
    list_filter = ['status', 'is_listed', 'blockchain', 'token_standard', 'category', 'created_at']
    search_fields = ['name', 'token_id', 'owner__username', 'creator__username']
    readonly_fields = ['created_at', 'updated_at', 'minted_at']
    filter_horizontal = ['tags']  
    inlines = [OwnershipHistoryInline] 


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'verified', 'total_volume', 'floor_price', 'created_at']
    list_filter = ['verified', 'created_at']
    search_fields = ['name', 'owner__username']

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['nft', 'seller', 'current_bid', 'start_time', 'end_time', 'active']
    list_filter = ['active', 'start_time', 'end_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(OwnershipHistory)
class OwnershipHistoryAdmin(admin.ModelAdmin):
    list_display = ['nft', 'owner', 'price', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['nft__name', 'owner__username', 'transaction_hash']