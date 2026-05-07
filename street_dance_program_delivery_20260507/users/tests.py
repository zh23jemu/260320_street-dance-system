from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from activities.models import Activity, ActivityRegistration
from mall.models import Order
from videos.models import Video

from .models import Favorite, Follow

User = get_user_model()


class UsersRouteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dancer01', password='StrongPass123')
        self.other_user = User.objects.create_user(username='dancer02', password='StrongPass123')

    def test_users_index_returns_ready(self):
        response = self.client.get(reverse('users-index'))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'module': 'users', 'status': 'ready'})

    def test_register_logs_user_in(self):
        response = self.client.post(
            reverse('users-register'),
            data={
                'username': 'dancer03',
                'password': 'StrongPass123',
                'confirm_password': 'StrongPass123',
                'nickname': 'Bboy One',
                'gender': 'male',
            },
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload['user']['username'], 'dancer03')
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_and_profile_update(self):
        user = User.objects.create_user(username='dancer04', password='StrongPass123')
        login_response = self.client.post(
            reverse('users-login'),
            data={'username': 'dancer04', 'password': 'StrongPass123'},
            content_type='application/json',
        )

        self.assertEqual(login_response.status_code, 200)

        update_response = self.client.patch(
            reverse('users-me'),
            data={'nickname': 'Locker', 'profile': '擅长 locking'},
            content_type='application/json',
        )

        self.assertEqual(update_response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.nickname, 'Locker')
        self.assertEqual(user.profile, '擅长 locking')

    def test_me_requires_login(self):
        response = self.client.get(reverse('users-me'))

        self.assertEqual(response.status_code, 401)

    def test_follow_and_lists(self):
        self.client.login(username='dancer01', password='StrongPass123')
        follow_response = self.client.post(reverse('users-follow', args=[self.other_user.id]))
        self.assertEqual(follow_response.status_code, 201)
        self.assertTrue(Follow.objects.filter(follower=self.user, following=self.other_user).exists())

        following_response = self.client.get(reverse('users-following'))
        self.assertEqual(len(following_response.json()['items']), 1)

        self.client.logout()
        self.client.login(username='dancer02', password='StrongPass123')
        followers_response = self.client.get(reverse('users-followers'))
        self.assertEqual(len(followers_response.json()['items']), 1)

    def test_dashboard_and_favorites(self):
        activity = Activity.objects.create(
            organizer=self.user,
            title='街舞海选',
            activity_type=Activity.ActivityType.COMPETITION,
            content='欢迎参加',
            location='上海',
            start_time=timezone.now() + timedelta(days=5),
            end_time=timezone.now() + timedelta(days=5, hours=2),
            signup_deadline=timezone.now() + timedelta(days=3),
            status=Activity.Status.PUBLISHED,
        )
        video = Video.objects.create(user=self.user, title='Demo', video_file='videos/demo.mp4')
        Order.objects.create(user=self.user, total_amount='99.00')
        ActivityRegistration.objects.create(activity=activity, user=self.other_user)
        Favorite.objects.create(user=self.user, target_type=Favorite.TargetType.ACTIVITY, target_id=activity.id)
        Favorite.objects.create(user=self.user, target_type=Favorite.TargetType.VIDEO, target_id=video.id)

        self.client.login(username='dancer01', password='StrongPass123')
        favorites_response = self.client.get(reverse('users-favorites'))
        self.assertEqual(len(favorites_response.json()['items']), 2)

        dashboard_response = self.client.get(reverse('users-dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        payload = dashboard_response.json()
        self.assertEqual(payload['counts']['published_activities'], 1)
        self.assertEqual(payload['counts']['videos'], 1)
        self.assertEqual(payload['counts']['favorites'], 2)
        self.assertEqual(payload['counts']['orders'], 1)
