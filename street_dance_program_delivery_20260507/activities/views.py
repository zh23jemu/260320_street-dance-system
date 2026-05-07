import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from users.models import Favorite

from .models import Activity, ActivityRegistration

User = get_user_model()


def _json_error(message, status=400):
    return JsonResponse({'detail': message}, status=status)


def _parse_json(request):
    if not request.body:
        return {}

    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


def _parse_client_datetime(value, field_name):
    dt = parse_datetime(value or '')
    if dt is None:
        raise ValueError(f'{field_name} 格式无效，请使用 ISO 8601 时间格式。')
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def _serialize_activity(activity, current_user=None):
    is_registered = False
    is_favorited = False
    if current_user and current_user.is_authenticated:
        is_registered = activity.registrations.filter(user=current_user).exists()
        is_favorited = Favorite.objects.filter(
            user=current_user,
            target_type=Favorite.TargetType.ACTIVITY,
            target_id=activity.id,
        ).exists()

    return {
        'id': activity.id,
        'title': activity.title,
        'activity_type': activity.activity_type,
        'content': activity.content,
        'location': activity.location,
        'latitude': float(activity.latitude) if activity.latitude is not None else None,
        'longitude': float(activity.longitude) if activity.longitude is not None else None,
        'start_time': activity.start_time.isoformat(),
        'end_time': activity.end_time.isoformat(),
        'signup_deadline': activity.signup_deadline.isoformat(),
        'status': activity.status,
        'organizer': {
            'id': activity.organizer_id,
            'username': activity.organizer.username,
            'nickname': activity.organizer.nickname,
        },
        'registration_count': activity.registrations.count(),
        'is_registered': is_registered,
        'is_favorited': is_favorited,
        'created_at': activity.created_at.isoformat(),
    }


@require_http_methods(['GET'])
def index(_request):
    return JsonResponse({'module': 'activities', 'status': 'ready'})


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def activity_list(request):
    if request.method == 'GET':
        queryset = Activity.objects.select_related('organizer').prefetch_related('registrations')
        keyword = (request.GET.get('keyword') or '').strip()
        activity_type = (request.GET.get('activity_type') or '').strip()
        status = (request.GET.get('status') or '').strip()

        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        if status:
            queryset = queryset.filter(status=status)

        data = [_serialize_activity(activity, request.user) for activity in queryset]
        return JsonResponse({'items': data})

    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    required_fields = ['title', 'activity_type', 'content', 'location', 'start_time', 'end_time', 'signup_deadline']
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        return _json_error(f'缺少必要字段: {", ".join(missing)}。')

    try:
        start_time = _parse_client_datetime(payload.get('start_time'), 'start_time')
        end_time = _parse_client_datetime(payload.get('end_time'), 'end_time')
        signup_deadline = _parse_client_datetime(payload.get('signup_deadline'), 'signup_deadline')
    except ValueError as exc:
        return _json_error(str(exc))

    if end_time <= start_time:
        return _json_error('活动结束时间必须晚于开始时间。')
    if signup_deadline > start_time:
        return _json_error('报名截止时间不能晚于活动开始时间。')

    activity = Activity.objects.create(
        organizer=request.user,
        title=payload['title'].strip(),
        activity_type=payload['activity_type'],
        content=payload['content'].strip(),
        location=payload['location'].strip(),
        latitude=payload.get('latitude'),
        longitude=payload.get('longitude'),
        start_time=start_time,
        end_time=end_time,
        signup_deadline=signup_deadline,
        status=payload.get('status') or Activity.Status.PUBLISHED,
    )
    return JsonResponse({'detail': '活动发布成功。', 'activity': _serialize_activity(activity, request.user)}, status=201)


@require_http_methods(['GET'])
def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity.objects.select_related('organizer').prefetch_related('registrations'), pk=activity_id)
    return JsonResponse({'activity': _serialize_activity(activity, request.user)})


@require_http_methods(['GET'])
def my_published(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    queryset = Activity.objects.filter(organizer=request.user).select_related('organizer').prefetch_related('registrations')
    return JsonResponse({'items': [_serialize_activity(activity, request.user) for activity in queryset]})


@require_http_methods(['GET'])
def my_registered(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    queryset = Activity.objects.filter(registrations__user=request.user).select_related('organizer').prefetch_related('registrations').distinct()
    return JsonResponse({'items': [_serialize_activity(activity, request.user) for activity in queryset]})


@csrf_exempt
@require_http_methods(['POST'])
def register_activity(request, activity_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    activity = get_object_or_404(Activity, pk=activity_id)
    if activity.signup_deadline < timezone.now():
        return _json_error('报名已截止。')

    registration, created = ActivityRegistration.objects.get_or_create(activity=activity, user=request.user)
    if not created:
        return _json_error('你已报名该活动。')

    return JsonResponse({'detail': '报名成功。', 'registration_id': registration.id}, status=201)


@csrf_exempt
@require_http_methods(['POST'])
def checkin_activity(request, activity_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    registration = get_object_or_404(ActivityRegistration, activity_id=activity_id, user=request.user)
    if registration.checked_in:
        return _json_error('你已签到。')

    registration.checked_in = True
    registration.checked_in_at = timezone.now()
    registration.save(update_fields=['checked_in', 'checked_in_at'])
    return JsonResponse({'detail': '签到成功。', 'checked_in_at': registration.checked_in_at.isoformat()})


@csrf_exempt
@require_http_methods(['POST'])
def favorite_activity(request, activity_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    activity = get_object_or_404(Activity, pk=activity_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        target_type=Favorite.TargetType.ACTIVITY,
        target_id=activity.id,
    )
    if not created:
        return _json_error('你已收藏该活动。')

    return JsonResponse({'detail': '收藏成功。', 'favorite_id': favorite.id}, status=201)
