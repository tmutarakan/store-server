from django.urls import path

from orders.views import OrderCreateView, SuccesTemplateView, CanceledTemplateView, OrderListView


app_name = 'orders'


urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order-success/', SuccesTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]
