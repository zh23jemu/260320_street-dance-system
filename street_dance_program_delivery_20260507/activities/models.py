from django.conf import settings
from django.db import models


class Activity(models.Model):
    class ActivityType(models.TextChoices):
        COMPETITION = 'competition', '比赛'
        COMMERCIAL = 'commercial', '商演'
        PERFORMANCE = 'performance', '表演'
        BACKUP_DANCER = 'backup_dancer', '伴舞'
        OTHER = 'other', '其他'

    class Status(models.TextChoices):
        DRAFT = 'draft', '草稿'
        PUBLISHED = 'published', '已发布'
        FINISHED = 'finished', '已结束'
        CANCELLED = 'cancelled', '已取消'

    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='published_activities')
    title = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices)
    cover_image = models.ImageField(upload_to='activities/', blank=True, null=True)
    content = models.TextField()
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    signup_deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_time', '-created_at']

    def __str__(self):
        return self.title


class ActivityRegistration(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_registrations')
    signup_time = models.DateTimeField(auto_now_add=True)
    checked_in = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-signup_time']
        unique_together = ('activity', 'user')

    def __str__(self):
        return f'{self.user} -> {self.activity}'
