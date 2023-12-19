from typing import Any
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Регистрация'
        return context


'''def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Вы успешно зарегистрированы!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)'''


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context
