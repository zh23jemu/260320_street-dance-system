import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import ChatMessage, ChatRoom

DEFAULT_ROOMS = [
    ('舞房招聘', ChatRoom.Category.STUDIO_RECRUITMENT),
    ('舞蹈心得交流', ChatRoom.Category.EXPERIENCE_SHARING),
    ('比赛经验', ChatRoom.Category.CONTEST_EXPERIENCE),
    ('Hiphop', ChatRoom.Category.HIPHOP),
    ('Swag', ChatRoom.Category.SWAG),
    ('Jazz', ChatRoom.Category.JAZZ),
    ('Popping', ChatRoom.Category.POPPING),
    ('Locking', ChatRoom.Category.LOCKING),
    ('Breaking', ChatRoom.Category.BREAKING),
    ('其他舞蹈分类', ChatRoom.Category.OTHER),
]


def _ensure_default_rooms():
    for room_name, category in DEFAULT_ROOMS:
        ChatRoom.objects.get_or_create(category=category, defaults={'room_name': room_name})


def _json_error(message, status=400):
    return JsonResponse({'detail': message}, status=status)


def _parse_json(request):
    if not request.body:
        return {}

    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


def _serialize_room(room):
    return {
        'id': room.id,
        'room_name': room.room_name,
        'category': room.category,
        'description': room.description,
        'created_at': room.created_at.isoformat(),
    }


def _serialize_message(message):
    return {
        'id': message.id,
        'content': message.content,
        'user': {
            'id': message.user_id,
            'username': message.user.username,
            'nickname': message.user.nickname,
        },
        'sent_at': message.sent_at.isoformat(),
    }


@require_http_methods(['GET'])
def index(_request):
    return JsonResponse({'module': 'social', 'status': 'ready'})


@require_http_methods(['GET'])
def room_list(_request):
    _ensure_default_rooms()
    rooms = ChatRoom.objects.all()
    return JsonResponse({'items': [_serialize_room(room) for room in rooms]})


@require_http_methods(['GET'])
def room_detail(_request, room_id):
    _ensure_default_rooms()
    room = get_object_or_404(ChatRoom, pk=room_id)
    messages = room.messages.select_related('user')
    return JsonResponse({'room': _serialize_room(room), 'messages': [_serialize_message(msg) for msg in messages]})


@csrf_exempt
@require_http_methods(['POST'])
def send_message(request, room_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    content = (payload.get('content') or '').strip()
    if not content:
        return _json_error('消息内容不能为空。')

    _ensure_default_rooms()
    room = get_object_or_404(ChatRoom, pk=room_id)
    message = ChatMessage.objects.create(room=room, user=request.user, content=content)
    return JsonResponse({'detail': '发送成功。', 'message': _serialize_message(message)}, status=201)
