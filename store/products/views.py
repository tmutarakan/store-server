from typing import Any
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from products.models import Product, ProductCategory, Basket
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = "products/index.html"
    title: str = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    context_object_name = "products"
    title: str = 'Store - Каталог'

    def get_queryset(self) -> QuerySet[Any]:
        queryset: QuerySet[Any] = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['categories'] = cache.get_or_set('categories', ProductCategory.objects.all(), 30)
        context['category_id']=self.kwargs.get('category_id')
        return context


@login_required
def basket_add(request, product_id):
    product: Product = Product.objects.get(id=product_id)
    baskets: BaseManager[Basket] = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket: Basket | None = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket: Basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
