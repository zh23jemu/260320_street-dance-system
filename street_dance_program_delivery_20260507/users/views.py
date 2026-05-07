import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from activities.models import Activity
from mall.models import Order
from videos.models import Video

from .models import Favorite, Follow, User


def _json_error(message, status=400):
    return JsonResponse({'detail': message}, status=status)


def _parse_json(request):
    if not request.body:
        return {}

    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


def _serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'email': user.email,
        'phone': user.phone,
        'gender': user.gender,
        'profile': user.profile,
        'is_staff': user.is_staff,
    }


def _serialize_activity(activity):
    return {
        'id': activity.id,
        'title': activity.title,
        'activity_type': activity.activity_type,
        'location': activity.location,
        'status': activity.status,
        'start_time': activity.start_time.isoformat(),
    }


def _serialize_video(video):
    return {
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'like_count': video.like_count,
        'favorite_count': video.favorite_count,
        'comment_count': video.comment_count,
        'created_at': video.created_at.isoformat(),
    }


def _serialize_order(order):
    return {
        'id': order.id,
        'total_amount': str(order.total_amount),
        'order_status': order.order_status,
        'payment_status': order.payment_status,
        'created_at': order.created_at.isoformat(),
    }


def _serialize_follow(relationship):
    target = relationship.following
    return {
        'id': relationship.id,
        'user': _serialize_user(target),
        'created_at': relationship.created_at.isoformat(),
    }


def _serialize_follower(relationship):
    source = relationship.follower
    return {
        'id': relationship.id,
        'user': _serialize_user(source),
        'created_at': relationship.created_at.isoformat(),
    }


@require_http_methods(['GET'])
def index(_request):
    return JsonResponse({'module': 'users', 'status': 'ready'})


@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    username = (payload.get('username') or '').strip()
    password = payload.get('password') or ''
    confirm_password = payload.get('confirm_password') or ''

    if not username or not password:
        return _json_error('用户名和密码不能为空。')
    if password != confirm_password:
        return _json_error('两次输入的密码不一致。')
    if User.objects.filter(username=username).exists():
        return _json_error('用户名已存在。')

    user = User.objects.create_user(
        username=username,
        password=password,
        email=(payload.get('email') or '').strip(),
        nickname=(payload.get('nickname') or '').strip(),
        phone=(payload.get('phone') or '').strip(),
        gender=payload.get('gender') or User.Gender.UNKNOWN,
        profile=(payload.get('profile') or '').strip(),
    )
    login(request, user)
    return JsonResponse({'detail': '注册成功。', 'user': _serialize_user(user)}, status=201)


@csrf_exempt
@require_http_methods(['POST'])
def login_view(request):
    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    username = (payload.get('username') or '').strip()
    password = payload.get('password') or ''
    user = authenticate(request, username=username, password=password)
    if user is None:
        return _json_error('用户名或密码错误。', status=401)

    login(request, user)
    return JsonResponse({'detail': '登录成功。', 'user': _serialize_user(user)})


@csrf_exempt
@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'detail': '退出登录成功。'})


@csrf_exempt
@require_http_methods(['GET', 'PATCH'])
def me(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    if request.method == 'GET':
        return JsonResponse({'user': _serialize_user(request.user)})

    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    editable_fields = []
    for field in ['nickname', 'email', 'phone', 'gender', 'profile']:
        if field in payload:
            value = payload[field]
            if field == 'gender' and value not in dict(User.Gender.choices):
                return _json_error('性别参数无效。')
            setattr(request.user, field, value.strip() if isinstance(value, str) else value)
            editable_fields.append(field)

    if editable_fields:
        request.user.save(update_fields=editable_fields)
    return JsonResponse({'detail': '个人信息已更新。', 'user': _serialize_user(request.user)})


@csrf_exempt
@require_http_methods(['POST'])
def follow_user(request, user_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)
    if request.user.id == user_id:
        return _json_error('不能关注自己。')

    target = get_object_or_404(User, pk=user_id)
    relationship, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        return _json_error('你已关注该用户。')
    return JsonResponse({'detail': '关注成功。', 'follow_id': relationship.id}, status=201)


@require_http_methods(['GET'])
def followers(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    queryset = Follow.objects.filter(following=request.user).select_related('follower')
    return JsonResponse({'items': [_serialize_follower(item) for item in queryset]})


@require_http_methods(['GET'])
def following(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    queryset = Follow.objects.filter(follower=request.user).select_related('following')
    return JsonResponse({'items': [_serialize_follow(item) for item in queryset]})


@require_http_methods(['GET'])
def favorites(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    favorites_qs = Favorite.objects.filter(user=request.user).order_by('-created_at')
    activity_ids = [item.target_id for item in favorites_qs if item.target_type == Favorite.TargetType.ACTIVITY]
    video_ids = [item.target_id for item in favorites_qs if item.target_type == Favorite.TargetType.VIDEO]

    activities = {item.id: item for item in Activity.objects.filter(id__in=activity_ids)}
    videos = {item.id: item for item in Video.objects.filter(id__in=video_ids)}

    items = []
    for item in favorites_qs:
        data = {
            'id': item.id,
            'target_type': item.target_type,
            'created_at': item.created_at.isoformat(),
        }
        if item.target_type == Favorite.TargetType.ACTIVITY and item.target_id in activities:
            data['target'] = _serialize_activity(activities[item.target_id])
            items.append(data)
        elif item.target_type == Favorite.TargetType.VIDEO and item.target_id in videos:
            data['target'] = _serialize_video(videos[item.target_id])
            items.append(data)

    return JsonResponse({'items': items})


@require_http_methods(['GET'])
def dashboard(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    published_activities = Activity.objects.filter(organizer=request.user)
    registered_activities = Activity.objects.filter(registrations__user=request.user).distinct()
    my_videos = Video.objects.filter(user=request.user)
    my_orders = Order.objects.filter(user=request.user)

    return JsonResponse(
        {
            'user': _serialize_user(request.user),
            'counts': {
                'published_activities': published_activities.count(),
                'registered_activities': registered_activities.count(),
                'videos': my_videos.count(),
                'favorites': Favorite.objects.filter(user=request.user).count(),
                'following': Follow.objects.filter(follower=request.user).count(),
                'followers': Follow.objects.filter(following=request.user).count(),
                'orders': my_orders.count(),
            },
            'latest': {
                'published_activities': [_serialize_activity(item) for item in published_activities[:5]],
                'registered_activities': [_serialize_activity(item) for item in registered_activities[:5]],
                'videos': [_serialize_video(item) for item in my_videos[:5]],
                'orders': [_serialize_order(item) for item in my_orders[:5]],
            },
        }
    )
