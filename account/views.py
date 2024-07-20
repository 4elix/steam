from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, EditProfileForm
from .models import Profile


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get("username")
                password = login_form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)

                    messages.success(request, 'Вы успешно вошли в аккаунт')
                    return redirect('home_path')
        else:
            login_form = LoginForm()
    else:
        messages.warning(request, 'Вы уже и так вошли в аккаунт')
        return redirect('home_path')
    content = {
        'login_form': login_form
    }
    return render(request, 'account/login.html', context=content)


def register_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            register_form = RegisterForm(data=request.POST)
            if register_form.is_valid():
                register_form = register_form.save()
                user = Profile.objects.create(user=register_form)
                user.save()

                messages.success(request, 'Вы создали аккаунт')
                return redirect('login')
        else:
            register_form = RegisterForm()
    else:
        messages.warning(request, 'Вы уже и так вошла в аккаунт')
        return redirect('home_path')
    content = {
        'register_form': register_form
    }
    return render(request, 'account/register.html', content)


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Вы вышли аккаунт')
        return redirect('home_path')
    else:
        messages.warning(request, 'Что бы выйти, нужно с начало зайти')
        return redirect('home_path')


def show_profile(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    content = {
        'profile': profile
    }
    return render(request, 'account/profile.html', content)


class EditProfile(UpdateView):
    form_class = EditProfileForm
    model = Profile
    template_name = 'account/edit_profile.html'
    extra_context = {
        'title': 'Изменения профиля'
    }

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'user_id': self.request.user.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)
