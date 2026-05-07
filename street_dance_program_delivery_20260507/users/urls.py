from django.urls import path

from .views import dashboard, favorites, followers, follow_user, following, index, login_view, logout_view, me, register

urlpatterns = [
    path('', index, name='users-index'),
    path('register/', register, name='users-register'),
    path('login/', login_view, name='users-login'),
    path('logout/', logout_view, name='users-logout'),
    path('me/', me, name='users-me'),
    path('dashboard/', dashboard, name='users-dashboard'),
    path('favorites/', favorites, name='users-favorites'),
    path('followers/', followers, name='users-followers'),
    path('following/', following, name='users-following'),
    path('<int:user_id>/follow/', follow_user, name='users-follow'),
]
