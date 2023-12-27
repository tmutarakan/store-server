from django.urls import path

from orders.views import OrderCreateView, SuccesTemplateView, CanceledTemplateView


app_name = 'orders'


urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccesTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]
