from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Favorite, Follow, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('nickname', 'avatar', 'gender', 'phone', 'profile')}),
    )
    list_display = ('username', 'nickname', 'email', 'phone', 'is_staff')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_type', 'target_id', 'created_at')
    list_filter = ('target_type',)
    search_fields = ('user__username',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
