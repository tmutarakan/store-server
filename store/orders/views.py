import json
from typing import Any
from uuid import uuid4
from http import HTTPStatus

from yookassa import Configuration, Payment

from django.conf import settings
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket


Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class SuccesTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created',)

    def get_queryset(self) -> QuerySet[Any]:
        queryset =  super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(TitleMixin, DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f"Store - Заказ №{self.object.id}"
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        super().post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        payment = Payment.create({
            "amount": {
                "value": baskets.total_sum(),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"{settings.DOMAIN_NAME}{reverse('orders:order_success')}"
            },
            "capture": True,
            "description": f"Заказ №{self.object.id}",
            "metadata": {'order_id': self.object.id}
        }, uuid4())
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.initiator = self.request.user
        return super().form_valid(form)


@csrf_exempt
def yookassa_webhook_view(request):
    payload = request.body.decode('utf-8')
    payload_dict = json.loads(payload)
    metadata = payload_dict['object']['metadata']
    print(f"Metadata: {metadata}")
    order_id = metadata['order_id']
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
    return HttpResponse(status=HTTPStatus.OK)
