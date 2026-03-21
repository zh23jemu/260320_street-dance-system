from django.conf import settings
from django.db import models


class ChatRoom(models.Model):
    class Category(models.TextChoices):
        STUDIO_RECRUITMENT = 'studio_recruitment', '舞房招聘'
        EXPERIENCE_SHARING = 'experience_sharing', '舞蹈心得交流'
        CONTEST_EXPERIENCE = 'contest_experience', '比赛经验'
        HIPHOP = 'hiphop', 'Hiphop'
        SWAG = 'swag', 'Swag'
        JAZZ = 'jazz', 'Jazz'
        POPPING = 'popping', 'Popping'
        LOCKING = 'locking', 'Locking'
        BREAKING = 'breaking', 'Breaking'
        OTHER = 'other', '其他'

    room_name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=Category.choices, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['room_name']

    def __str__(self):
        return self.room_name


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f'{self.user} @ {self.room}'
