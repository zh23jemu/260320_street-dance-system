from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from users.models import Favorite

from .models import Activity, ActivityRegistration

User = get_user_model()


class ActivitiesRouteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='organizer', password='StrongPass123')
        self.other_user = User.objects.create_user(username='guest', password='StrongPass123')
        now = timezone.now()
        self.activity = Activity.objects.create(
            organizer=self.user,
            title='街舞公开赛',
            activity_type=Activity.ActivityType.COMPETITION,
            content='欢迎报名参加比赛',
            location='上海市静安区',
            start_time=now + timedelta(days=7),
            end_time=now + timedelta(days=7, hours=4),
            signup_deadline=now + timedelta(days=5),
            status=Activity.Status.PUBLISHED,
        )

    def test_activities_index_returns_ready(self):
        response = self.client.get(reverse('activities-index'))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'module': 'activities', 'status': 'ready'})

    def test_create_activity_requires_login(self):
        response = self.client.post(
            reverse('activities-list'),
            data={'title': '未登录活动'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_create_activity(self):
        self.client.login(username='organizer', password='StrongPass123')
        response = self.client.post(
            reverse('activities-list'),
            data={
                'title': 'Freestyle Jam',
                'activity_type': Activity.ActivityType.PERFORMANCE,
                'content': '开放报名',
                'location': '上海市黄浦区',
                'start_time': (timezone.now() + timedelta(days=10)).isoformat(),
                'end_time': (timezone.now() + timedelta(days=10, hours=2)).isoformat(),
                'signup_deadline': (timezone.now() + timedelta(days=8)).isoformat(),
            },
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Activity.objects.count(), 2)

    def test_user_can_register_check_in_and_favorite(self):
        self.client.login(username='guest', password='StrongPass123')
        register_response = self.client.post(reverse('activities-register', args=[self.activity.id]))
        self.assertEqual(register_response.status_code, 201)
        self.assertTrue(ActivityRegistration.objects.filter(activity=self.activity, user=self.other_user).exists())

        checkin_response = self.client.post(reverse('activities-checkin', args=[self.activity.id]))
        self.assertEqual(checkin_response.status_code, 200)

        favorite_response = self.client.post(reverse('activities-favorite', args=[self.activity.id]))
        self.assertEqual(favorite_response.status_code, 201)
        self.assertTrue(Favorite.objects.filter(user=self.other_user, target_id=self.activity.id).exists())

        registration = ActivityRegistration.objects.get(activity=self.activity, user=self.other_user)
        self.assertTrue(registration.checked_in)

    def test_my_lists_return_expected_records(self):
        ActivityRegistration.objects.create(activity=self.activity, user=self.other_user)
        self.client.login(username='organizer', password='StrongPass123')
        published_response = self.client.get(reverse('activities-my-published'))
        self.assertEqual(len(published_response.json()['items']), 1)

        self.client.logout()
        self.client.login(username='guest', password='StrongPass123')
        registered_response = self.client.get(reverse('activities-my-registered'))
        self.assertEqual(len(registered_response.json()['items']), 1)
