from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'male', '男'
        FEMALE = 'female', '女'
        OTHER = 'other', '其他'
        UNKNOWN = 'unknown', '保密'

    nickname = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.UNKNOWN)
    phone = models.CharField(max_length=20, blank=True)
    profile = models.TextField(blank=True)

    def __str__(self):
        return self.nickname or self.username


class Favorite(models.Model):
    class TargetType(models.TextChoices):
        ACTIVITY = 'activity', '活动'
        VIDEO = 'video', '视频'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorites')
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'target_type', 'target_id')

    def __str__(self):
        return f'{self.user} -> {self.target_type}:{self.target_id}'


class Follow(models.Model):
    follower = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='following_relationships')
    following = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='follower_relationships')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'
