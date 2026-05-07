from django.urls import path

from .views import index, room_detail, room_list, send_message

urlpatterns = [
    path('', index, name='social-index'),
    path('rooms/', room_list, name='social-room-list'),
    path('rooms/<int:room_id>/', room_detail, name='social-room-detail'),
    path('rooms/<int:room_id>/messages/', send_message, name='social-send-message'),
]
