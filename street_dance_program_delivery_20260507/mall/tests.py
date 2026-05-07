from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import CartItem, Order, Product

User = get_user_model()


class MallRouteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='StrongPass123')
        self.product = Product.objects.create(
            name='街舞卫衣',
            category='服装',
            price=Decimal('199.00'),
            stock=10,
            description='宽松版型',
            status=Product.Status.ON_SALE,
        )

    def test_mall_index_returns_ready(self):
        response = self.client.get(reverse('mall-index'))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'module': 'mall', 'status': 'ready'})

    def test_authenticated_user_can_add_to_cart(self):
        self.client.login(username='buyer', password='StrongPass123')
        response = self.client.post(
            reverse('mall-cart'),
            data={'product_id': self.product.id, 'quantity': 2},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(CartItem.objects.filter(user=self.user, product=self.product).exists())

    def test_user_can_create_and_pay_order(self):
        self.client.login(username='buyer', password='StrongPass123')
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)

        create_response = self.client.post(reverse('mall-create-order'))
        self.assertEqual(create_response.status_code, 201)
        order_id = create_response.json()['order']['id']

        pay_response = self.client.post(reverse('mall-pay-order', args=[order_id]))
        self.assertEqual(pay_response.status_code, 200)

        order = Order.objects.get(pk=order_id)
        self.assertTrue(order.payment_status)
        self.assertEqual(order.order_status, Order.OrderStatus.PAID)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
