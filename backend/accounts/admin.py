from django.contrib import admin
from .models import User, UserProfile
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone', 'role', 'is_staff', 'is_active')  
    search_fields = ('first_name', 'last_name','username' )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('username',)  
    
        
    fieldsets = (
            (_("Main info"), {"fields": ("username", "email", "phone", "role")}),
            (_("Personal details"), {"fields": ("first_name", "last_name")}),
            (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
            (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        )
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('username',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_address')  
    search_fields = ('user__username', 'wallet_address')
    ordering = ('user__username',)