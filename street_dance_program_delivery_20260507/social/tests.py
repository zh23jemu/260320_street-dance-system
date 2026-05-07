from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ChatMessage, ChatRoom

User = get_user_model()


class SocialRouteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='chatter', password='StrongPass123')

    def test_social_index_returns_ready(self):
        response = self.client.get(reverse('social-index'))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'module': 'social', 'status': 'ready'})

    def test_room_list_bootstraps_default_rooms(self):
        response = self.client.get(reverse('social-room-list'))

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()['items']), 10)
        self.assertTrue(ChatRoom.objects.exists())

    def test_authenticated_user_can_send_message(self):
        room_list_response = self.client.get(reverse('social-room-list'))
        room_id = room_list_response.json()['items'][0]['id']

        self.client.login(username='chatter', password='StrongPass123')
        response = self.client.post(
            reverse('social-send-message', args=[room_id]),
            data={'content': '有没有周末约练？'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(ChatMessage.objects.filter(room_id=room_id, user=self.user).exists())
