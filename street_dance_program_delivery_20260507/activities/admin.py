from django.contrib import admin

from .models import Activity, ActivityRegistration


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'organizer', 'start_time', 'status')
    list_filter = ('activity_type', 'status')
    search_fields = ('title', 'location', 'organizer__username')


@admin.register(ActivityRegistration)
class ActivityRegistrationAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'signup_time', 'checked_in')
    list_filter = ('checked_in',)
    search_fields = ('activity__title', 'user__username')
