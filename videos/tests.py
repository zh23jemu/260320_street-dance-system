from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.models import Favorite

from .models import Video, VideoComment

User = get_user_model()


class VideosRouteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='videouser', password='StrongPass123')
        self.video = Video.objects.create(
            user=self.user,
            title='Routine Demo',
            video_file='videos/demo.mp4',
            description='编舞展示',
        )

    def test_videos_index_returns_ready(self):
        response = self.client.get(reverse('videos-index'))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'module': 'videos', 'status': 'ready'})

    def test_authenticated_user_can_create_video(self):
        self.client.login(username='videouser', password='StrongPass123')
        response = self.client.post(
            reverse('videos-list'),
            data={'title': 'Battle Clip', 'video_file': 'videos/battle.mp4', 'description': '比赛片段'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Video.objects.count(), 2)

    def test_user_can_like_favorite_and_comment_video(self):
        self.client.login(username='videouser', password='StrongPass123')

        like_response = self.client.post(reverse('videos-like', args=[self.video.id]))
        self.assertEqual(like_response.status_code, 200)

        favorite_response = self.client.post(reverse('videos-favorite', args=[self.video.id]))
        self.assertEqual(favorite_response.status_code, 201)
        self.assertTrue(Favorite.objects.filter(target_id=self.video.id).exists())

        comment_response = self.client.post(
            reverse('videos-comment', args=[self.video.id]),
            data={'content': '跳得很稳'},
            content_type='application/json',
        )
        self.assertEqual(comment_response.status_code, 201)
        self.assertTrue(VideoComment.objects.filter(video=self.video).exists())

        self.video.refresh_from_db()
        self.assertEqual(self.video.like_count, 1)
        self.assertEqual(self.video.favorite_count, 1)
        self.assertEqual(self.video.comment_count, 1)
