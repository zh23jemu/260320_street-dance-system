from django.urls import path

from .views import comment_video, favorite_video, index, like_video, my_videos, video_detail, video_list

urlpatterns = [
    path('', index, name='videos-index'),
    path('list/', video_list, name='videos-list'),
    path('my/', my_videos, name='videos-my'),
    path('<int:video_id>/', video_detail, name='videos-detail'),
    path('<int:video_id>/like/', like_video, name='videos-like'),
    path('<int:video_id>/favorite/', favorite_video, name='videos-favorite'),
    path('<int:video_id>/comments/', comment_video, name='videos-comment'),
]
