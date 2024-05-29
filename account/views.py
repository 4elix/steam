from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import success

from .forms import RegisterForm, LoginForm


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                success(request, 'Вы успешно вошли в аккаунт')
                return redirect('home_page')
    else:
        login_form = LoginForm()

    content = {
        'login_form': login_form
    }
    return render(request, 'login.html', context=content)


def register_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            success(request, 'Вы создали аккаунт')
            return redirect('login')
    else:
        register_form = RegisterForm()

    content = {
        'register_form': register_form
    }
    return render(request, 'register.html', content)


def user_logout(request):
    logout(request)
    success(request, 'Вы вышли аккаунт')
    return redirect("home_page")
