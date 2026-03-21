from django.contrib import admin

from .models import Video, VideoComment


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'like_count', 'favorite_count', 'created_at')
    search_fields = ('title', 'user__username')


@admin.register(VideoComment)
class VideoCommentAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'created_at')
    search_fields = ('video__title', 'user__username')
