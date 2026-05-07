import json
from decimal import Decimal

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CartItem, Order, OrderItem, Product


def _json_error(message, status=400):
    return JsonResponse({'detail': message}, status=status)


def _parse_json(request):
    if not request.body:
        return {}

    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


def _serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'category': product.category,
        'price': str(product.price),
        'stock': product.stock,
        'description': product.description,
        'status': product.status,
        'created_at': product.created_at.isoformat(),
    }


def _serialize_cart_item(item):
    return {
        'id': item.id,
        'quantity': item.quantity,
        'product': _serialize_product(item.product),
        'subtotal': str(item.product.price * item.quantity),
    }


def _serialize_order(order):
    return {
        'id': order.id,
        'total_amount': str(order.total_amount),
        'order_status': order.order_status,
        'payment_status': order.payment_status,
        'items': [
            {
                'id': item.id,
                'quantity': item.quantity,
                'unit_price': str(item.unit_price),
                'product': _serialize_product(item.product),
            }
            for item in order.items.select_related('product')
        ],
        'created_at': order.created_at.isoformat(),
    }


@require_http_methods(['GET'])
def index(_request):
    return JsonResponse({'module': 'mall', 'status': 'ready'})


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.all()
        keyword = (request.GET.get('keyword') or '').strip()
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        return JsonResponse({'items': [_serialize_product(product) for product in queryset]})

    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    required_fields = ['name', 'category', 'price', 'stock']
    missing = [field for field in required_fields if payload.get(field) in (None, '')]
    if missing:
        return _json_error(f'缺少必要字段: {", ".join(missing)}。')

    product = Product.objects.create(
        name=(payload.get('name') or '').strip(),
        category=(payload.get('category') or '').strip(),
        price=Decimal(str(payload.get('price'))),
        stock=int(payload.get('stock')),
        description=(payload.get('description') or '').strip(),
        status=payload.get('status') or Product.Status.ON_SALE,
    )
    return JsonResponse({'detail': '商品创建成功。', 'product': _serialize_product(product)}, status=201)


@require_http_methods(['GET'])
def product_detail(_request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return JsonResponse({'product': _serialize_product(product)})


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def cart_items(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    if request.method == 'GET':
        items = CartItem.objects.filter(user=request.user).select_related('product')
        return JsonResponse({'items': [_serialize_cart_item(item) for item in items]})

    payload = _parse_json(request)
    if payload is None:
        return _json_error('请求体必须是合法 JSON。')

    product = get_object_or_404(Product, pk=payload.get('product_id'))
    quantity = int(payload.get('quantity') or 1)
    if quantity <= 0:
        return _json_error('商品数量必须大于 0。')
    if product.stock < quantity:
        return _json_error('库存不足。')

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity},
    )
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            return _json_error('库存不足。')
        cart_item.save(update_fields=['quantity'])

    return JsonResponse({'detail': '已加入购物车。', 'item': _serialize_cart_item(cart_item)}, status=201)


@csrf_exempt
@require_http_methods(['POST'])
def create_order(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    cart_qs = CartItem.objects.filter(user=request.user).select_related('product')
    cart_items_list = list(cart_qs)
    if not cart_items_list:
        return _json_error('购物车为空。')

    with transaction.atomic():
        total_amount = Decimal('0.00')
        order = Order.objects.create(user=request.user, total_amount=Decimal('0.00'))

        for cart_item in cart_items_list:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                raise ValueError(f'{product.name} 库存不足。')
            product.stock -= cart_item.quantity
            product.save(update_fields=['stock'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                unit_price=product.price,
            )
            total_amount += product.price * cart_item.quantity

        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])
        cart_qs.delete()

    return JsonResponse({'detail': '订单创建成功。', 'order': _serialize_order(order)}, status=201)


@csrf_exempt
@require_http_methods(['POST'])
def pay_order(request, order_id):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    order = get_object_or_404(Order.objects.prefetch_related('items__product'), pk=order_id, user=request.user)
    if order.payment_status:
        return _json_error('订单已支付。')

    order.payment_status = True
    order.order_status = Order.OrderStatus.PAID
    order.save(update_fields=['payment_status', 'order_status'])
    return JsonResponse({'detail': '模拟支付成功。', 'order': _serialize_order(order)})


@require_http_methods(['GET'])
def my_orders(request):
    if not request.user.is_authenticated:
        return _json_error('请先登录。', status=401)

    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return JsonResponse({'items': [_serialize_order(order) for order in orders]})
