from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from activities.models import Activity, ActivityRegistration
from mall.models import CartItem, Order, OrderItem, Product
from social.models import ChatMessage, ChatRoom
from users.models import Favorite, Follow
from videos.models import Video, VideoComment


User = get_user_model()


class Command(BaseCommand):
    help = 'Seed demo data for the street dance system.'

    def handle(self, *args, **options):
        now = timezone.now()

        admin_user, _ = User.objects.get_or_create(
            username='admin_demo',
            defaults={
                'nickname': '平台管理员',
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
                'phone': '13800000000',
                'profile': '负责演示数据维护',
            },
        )
        admin_user.set_password('Admin123456')
        admin_user.save()

        dancer, _ = User.objects.get_or_create(
            username='bboy_chen',
            defaults={
                'nickname': 'Bboy Chen',
                'email': 'bboychen@example.com',
                'phone': '13900000001',
                'profile': '擅长 breaking 和 freestyle',
            },
        )
        dancer.set_password('Dance123456')
        dancer.save()

        organizer, _ = User.objects.get_or_create(
            username='studio_muse',
            defaults={
                'nickname': 'Muse Studio',
                'email': 'muse@example.com',
                'phone': '13900000002',
                'profile': '主办赛事和公开课活动',
            },
        )
        organizer.set_password('Dance123456')
        organizer.save()

        viewer, _ = User.objects.get_or_create(
            username='jazz_luna',
            defaults={
                'nickname': 'Jazz Luna',
                'email': 'luna@example.com',
                'phone': '13900000003',
                'profile': '喜欢 Jazz 和编舞分享',
            },
        )
        viewer.set_password('Dance123456')
        viewer.save()

        Follow.objects.get_or_create(follower=viewer, following=dancer)
        Follow.objects.get_or_create(follower=dancer, following=organizer)

        activity_1, _ = Activity.objects.get_or_create(
            organizer=organizer,
            title='2026 上海街舞公开赛',
            defaults={
                'activity_type': Activity.ActivityType.COMPETITION,
                'content': '面向 Hiphop、Breaking、Popping 选手开放报名。',
                'location': '上海市黄浦区街舞中心',
                'start_time': now + timedelta(days=10),
                'end_time': now + timedelta(days=10, hours=6),
                'signup_deadline': now + timedelta(days=7),
                'status': Activity.Status.PUBLISHED,
            },
        )
        activity_2, _ = Activity.objects.get_or_create(
            organizer=organizer,
            title='周末 Jazz 编舞公开课',
            defaults={
                'activity_type': Activity.ActivityType.PERFORMANCE,
                'content': '适合初中级舞者，现场分组练习。',
                'location': '上海市静安区舞蹈工坊',
                'start_time': now + timedelta(days=5),
                'end_time': now + timedelta(days=5, hours=3),
                'signup_deadline': now + timedelta(days=3),
                'status': Activity.Status.PUBLISHED,
            },
        )

        registration, _ = ActivityRegistration.objects.get_or_create(activity=activity_1, user=dancer)
        if not registration.checked_in:
            registration.checked_in = True
            registration.checked_in_at = now
            registration.save(update_fields=['checked_in', 'checked_in_at'])
        ActivityRegistration.objects.get_or_create(activity=activity_2, user=viewer)

        video_1, _ = Video.objects.get_or_create(
            user=dancer,
            title='Breaking Showcase 2026',
            defaults={
                'video_file': 'videos/breaking-showcase.mp4',
                'description': '训练室版本作品记录',
                'like_count': 18,
                'favorite_count': 6,
                'comment_count': 0,
            },
        )
        video_2, _ = Video.objects.get_or_create(
            user=viewer,
            title='Jazz Choreo Demo',
            defaults={
                'video_file': 'videos/jazz-demo.mp4',
                'description': '公开课课后作品',
                'like_count': 9,
                'favorite_count': 4,
                'comment_count': 0,
            },
        )

        comment_1, created = VideoComment.objects.get_or_create(
            video=video_1,
            user=viewer,
            content='这段 power move 很干净。',
        )
        comment_2, _ = VideoComment.objects.get_or_create(
            video=video_2,
            user=dancer,
            content='节奏处理很舒服。',
        )
        if created:
            video_1.comment_count = video_1.comments.count()
            video_1.save(update_fields=['comment_count'])
        video_2.comment_count = video_2.comments.count()
        video_2.save(update_fields=['comment_count'])

        Favorite.objects.get_or_create(
            user=viewer,
            target_type=Favorite.TargetType.ACTIVITY,
            target_id=activity_1.id,
        )
        Favorite.objects.get_or_create(
            user=viewer,
            target_type=Favorite.TargetType.VIDEO,
            target_id=video_1.id,
        )

        rooms = [
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
        created_rooms = {}
        for room_name, category in rooms:
            room, _ = ChatRoom.objects.get_or_create(
                category=category,
                defaults={'room_name': room_name},
            )
            created_rooms[category] = room

        ChatMessage.objects.get_or_create(
            room=created_rooms[ChatRoom.Category.BREAKING],
            user=dancer,
            content='这周六有人一起约练风车吗？',
        )
        ChatMessage.objects.get_or_create(
            room=created_rooms[ChatRoom.Category.JAZZ],
            user=viewer,
            content='最近在练线条控制，有没有推荐的基础训练？',
        )

        hoodie, _ = Product.objects.get_or_create(
            name='街舞卫衣',
            defaults={
                'category': '服装',
                'price': Decimal('199.00'),
                'stock': 20,
                'description': '宽松剪裁，适合排练和日常穿搭',
                'status': Product.Status.ON_SALE,
            },
        )
        pants, _ = Product.objects.get_or_create(
            name='训练长裤',
            defaults={
                'category': '服装',
                'price': Decimal('169.00'),
                'stock': 15,
                'description': '耐磨面料，适合地板动作训练',
                'status': Product.Status.ON_SALE,
            },
        )
        cap, _ = Product.objects.get_or_create(
            name='演出鸭舌帽',
            defaults={
                'category': '配件',
                'price': Decimal('89.00'),
                'stock': 30,
                'description': '基础百搭款',
                'status': Product.Status.ON_SALE,
            },
        )

        cart_item, _ = CartItem.objects.get_or_create(user=viewer, product=hoodie, defaults={'quantity': 1})
        if cart_item.quantity != 1:
            cart_item.quantity = 1
            cart_item.save(update_fields=['quantity'])

        order, _ = Order.objects.get_or_create(
            user=viewer,
            total_amount=Decimal('258.00'),
            defaults={
                'order_status': Order.OrderStatus.PAID,
                'payment_status': True,
            },
        )
        OrderItem.objects.get_or_create(
            order=order,
            product=pants,
            defaults={'quantity': 1, 'unit_price': pants.price},
        )
        OrderItem.objects.get_or_create(
            order=order,
            product=cap,
            defaults={'quantity': 1, 'unit_price': cap.price},
        )

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
        self.stdout.write('Admin: admin_demo / Admin123456')
        self.stdout.write('Users: bboy_chen, studio_muse, jazz_luna / Dance123456')
