import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from users.models import Favorite

from .models import Video, VideoComment


def _json_error(message, status=400):
    return JsonResponse({'detail': message}, status=status)


def _parse_json(request):
    if not request.body:
        return {}

    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


def _serialize_video(video, current_user=None):
    is_favorited = False
    if current_user and current_user.is_authenticated:
        is_favorited = Favorite.objects.filter(
            user=current_user,
            target_type=Favorite.TargetType.VIDEO,
            target_id=video.id,
        ).exists()

    return {
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'video_file': video.video_file.name,
        'cover_image': video.cover_image.name if video.cover_image else None,
        'like_count': video.like_count,
        'favorite_count': video.favorite_count,
        'comment_count': video.comment_count,
        'user': {
            'id': video.user_id,
            'username': video.user.username,
            'nickname': video.user.nickname,
        },
        'is_favorited': is_favorited,
        'created_at': video.created_at.isoformat(),
    }


def _serialize_comment(comment):
    return {
        'id': comment.id,
        'content': comment.content,
        'user': {
            'id': comment.user_id,
            'username': comment.user.username,
            'nickname': comment.user.nickname,
        },
        'created_at': comment.created_at.isoformat(),
    }


@require_http_methods(['GET'])
def index(_request):
    return JsonResponse({'module': 'videos', 'status': 'ready'})


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def video_list(request):
    if request.method == 'GET':
        queryset = Video.objects.select_related('user')
        keyword = (request.GET.get('keyword') or '').strip()
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        return JsonResponse({'items': [_serialize_video(video, request.user) for video in queryset]})

    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    title = (payload.get('title') or '').strip()
    video_file = (payload.get('video_file') or '').strip()
    if not title or not video_file:
        return _json_error('标题和视频地址不能为空。')

    video = Video.objects.create(
        user=request.user,
        title=title,
        video_file=video_file,
        description=(payload.get('description') or '').strip(),
    )
    return JsonResponse({'detail': '视频发布成功。', 'video': _serialize_video(video, request.user)}, status=201)


@require_http_methods(['GET'])
def video_detail(request, video_id):
    video = get_object_or_404(Video.objects.select_related('user'), pk=video_id)
    comments = VideoComment.objects.filter(video=video).select_related('user')
    return JsonResponse(
        {
            'video': _serialize_video(video, request.user),
            'comments': [_serialize_comment(comment) for comment in comments],
        }
    )


@require_http_methods(['GET'])
def my_videos(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    queryset = Video.objects.filter(user=request.user).select_related('user')
    return JsonResponse({'items': [_serialize_video(video, request.user) for video in queryset]})


@csrf_exempt
@require_http_methods(['POST'])
def like_video(request, video_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    video = get_object_or_404(Video, pk=video_id)
    video.like_count += 1
    video.save(update_fields=['like_count'])
    return JsonResponse({'detail': '点赞成功。', 'like_count': video.like_count})


@csrf_exempt
@require_http_methods(['POST'])
def favorite_video(request, video_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    video = get_object_or_404(Video, pk=video_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        target_type=Favorite.TargetType.VIDEO,
        target_id=video.id,
    )
    if not created:
        return _json_error('你已收藏该视频。')

    video.favorite_count += 1
    video.save(update_fields=['favorite_count'])
    return JsonResponse({'detail': '收藏成功。', 'favorite_id': favorite.id, 'favorite_count': video.favorite_count}, status=201)


@csrf_exempt
@require_http_methods(['POST'])
def comment_video(request, video_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    content = (payload.get('content') or '').strip()
    if not content:
        return _json_error('评论内容不能为空。')

    video = get_object_or_404(Video, pk=video_id)
    comment = VideoComment.objects.create(video=video, user=request.user, content=content)
    video.comment_count += 1
    video.save(update_fields=['comment_count'])
    return JsonResponse({'detail': '评论成功。', 'comment': _serialize_comment(comment)}, status=201)
