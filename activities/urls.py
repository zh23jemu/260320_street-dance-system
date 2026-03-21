from django.urls import path

from .views import activity_detail, activity_list, checkin_activity, favorite_activity, index, my_published, my_registered, register_activity

urlpatterns = [
    path('', index, name='activities-index'),
    path('list/', activity_list, name='activities-list'),
    path('my/published/', my_published, name='activities-my-published'),
    path('my/registered/', my_registered, name='activities-my-registered'),
    path('<int:activity_id>/', activity_detail, name='activities-detail'),
    path('<int:activity_id>/register/', register_activity, name='activities-register'),
    path('<int:activity_id>/checkin/', checkin_activity, name='activities-checkin'),
    path('<int:activity_id>/favorite/', favorite_activity, name='activities-favorite'),
]
