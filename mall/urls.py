from django.urls import path

from .views import cart_items, create_order, index, my_orders, pay_order, product_detail, product_list

urlpatterns = [
    path('', index, name='mall-index'),
    path('products/', product_list, name='mall-product-list'),
    path('products/<int:product_id>/', product_detail, name='mall-product-detail'),
    path('cart/', cart_items, name='mall-cart'),
    path('orders/', my_orders, name='mall-orders'),
    path('orders/create/', create_order, name='mall-create-order'),
    path('orders/<int:order_id>/pay/', pay_order, name='mall-pay-order'),
]
