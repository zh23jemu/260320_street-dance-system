from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(_request):
    return JsonResponse({'status': 'ok', 'project': 'street-dance-system'})


urlpatterns = [
    path('', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('activities/', include('activities.urls')),
    path('videos/', include('videos.urls')),
    path('social/', include('social.urls')),
    path('mall/', include('mall.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
