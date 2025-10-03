from django.contrib import admin
from .models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone')  
    search_fields = ('first_name', 'last_name','username' )  
    
fieldsets = (
        (_("Main info"), {"fields": ("username", "email", "phone", "role")}),
        (_("Personal details"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )