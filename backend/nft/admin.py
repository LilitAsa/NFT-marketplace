from django.conf import settings
from django.contrib import admin
from .models import *
from django.utils.html import format_html



class OwnershipHistoryInline(admin.TabularInline):
    model = OwnershipHistory
    extra = 0
    readonly_fields = ['timestamp']

@admin.register(NFT)
class NFTAdmin(admin.ModelAdmin):
    list_display = ['name', 'token_id', 'owner', 'creator', 'status', 'is_listed', 'price', 'created_at', 'image_file']
    list_filter = ['status', 'is_listed', 'blockchain', 'token_standard', 'category', 'created_at']
    search_fields = ['name', 'token_id', 'owner__username', 'creator__username']
    readonly_fields = ['created_at', 'updated_at', 'minted_at']
    filter_horizontal = ['tags']  
    inlines = [OwnershipHistoryInline] 
    # fields = (
    #     ('name', 'token_id'),
    #     ('owner', 'creator'),
    #     ('image', 'image_file'),
    #     ('description', 'external_url'),
    #     ('price', 'currency', 'is_listed', 'status'),
    #     ('contract_address', 'blockchain', 'token_standard'),
    # )
    
 # Preview for edit page
    def image_preview(self, obj):
        src = ""
        if obj.image_file:
            try:
                src = obj.image_file.url
            except:
                src = ""
        elif obj.image:
            src = obj.image
        else:
            src = settings.MEDIA_URL + "nft_images/placeholder-nft.png"

        return format_html(
            '<img src="{}" style="max-height:160px; border-radius:10px; margin-top:10px" />', src
        )

    image_preview.short_description = "Preview"

    # Preview in list
    def preview_small(self, obj):
        if obj.image_file:
            url = obj.image_file.url
        elif obj.image:
            url = obj.image
        else:
            url = settings.MEDIA_URL + "nft_images/placeholder-nft.png"

        return format_html('<img src="{}" style="height:40px;border-radius:4px"/>', url)

    preview_small.short_description = ""
    


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