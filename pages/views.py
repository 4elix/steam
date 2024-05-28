from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import success
from django.http import HttpResponse, FileResponse

from .models import Categories, Products, Favorite, Review
from .forms import RegisterForm, LoginForm, ReviewForm


def index_page(request):
    # имя_таблицы.объекты.все
    # переменная которая забирает из таблицы все данные
    categories = Categories.objects.all()
    games = Products.objects.all()
    games_discount = [i for i in games if i.discount > 0]
    # данный словарь хранит в себе ключи, к котором можно обращаться внутри
    # указанного шаблона для получения списка с данными
    content = {
        'categories': categories,
        'games': games[2:5][::-1],
        'games_discount': games_discount
    }
    # return render(request, 'путь к шаблону', context=переменная отвечающая
    # за вывод списка который хранит в себе QuerySet
    return render(request, 'index.html', context=content)


def show_game_by_cat_id(request, cat_id):
    # url адрес http://127.0.0.1:8000/category/1
    # параметр cat_id будет забирать из адреса цифру,
    # по этой цифре мы найдем нужную категорию, а потом буд
    # фильтровать играм по нужной категории и получать QuerySet статей

    # filter -> отдаст несколько значений

    games = Products.objects.filter(category_id=cat_id)
    categories = Categories.objects.all()
    content = {
        'games': games,
        'categories': categories
    }
    return render(request, 'index.html', content)


def show_detail(request, slug_path):
    # url адрес: http://127.0.0.1:8000/game/detail/Sekiro_Shadows_Die_Twice/

    # get -> берет одни объект подходящий под условия

    # game = Products.objects.get(slug=slug_path)

    # или

    # get_object_or_404 -> данная функция отдаст объект
    # или выдаст страницу 404, с начало мы указываем модельку,
    # потом аргументы
    game = get_object_or_404(Products, slug=slug_path)

    comments = game.comments.filter(parent=None)
    if request.method == "POST":
        comment_form = ReviewForm(data=request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.auth = request.user
            comment_form.product = game
            comment_form.save()
            return redirect('detail', game.slug)
    else:
        comment_form = ReviewForm()

    content = {
        'game': game,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'detail.html', content)


def login_view(request):
    # проверка метода на POST
    if request.method == 'POST':
        # в форму передаем данный
        login_form = LoginForm(data=request.POST)
        # проверяем на валидность
        if login_form.is_valid():
            # забирам логин и пароль
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            # с помощью функции, входим в аккаунт
            user = authenticate(username=username, password=password)
            if user is not None:
                # Сохраняйте идентификатор пользователя и серверную часть в запросе. Таким образом, пользователю не
                # нужно повторно проходить аутентификацию при каждом запросе.
                login(request, user)

                # функция для отправки сообщения
                success(request, 'Вы успешно вошли в аккаунт')
                # redirect -> функция для того что перенаправлять на имени ссылки
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
    # функция по запросу выходит с аккаунта
    logout(request)
    success(request, 'Вы вышли аккаунт')
    return redirect("home_page")


def add_reply(request, pk):
    comment = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        comment_form = ReviewForm(data=request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.auth = request.user
            comment_form.product = comment.product
            comment_form.parent = comment
            comment_form.save()
            return redirect('detail', comment.product.slug)
    else:
        comment_form = ReviewForm()

    content = {
        'comment_form': comment_form
    }
    return render(request, 'detail.html', content)


def like_logik(request, pk_product):
    if request.user.is_authenticated:
        user = request.user

        # находиться ли игра в фаворитах, мы получаем True, False.
        # это все благодаря .exists()
        status = Favorite.objects.filter(auth=user, product_id=pk_product).exists()
        if status:
            like = Favorite.objects.get(auth=user, product_id=pk_product)
            # delete удаляет запись, если мы повторно нажимаем на сердечко
            like.delete()
        else:
            like = Favorite.objects.create(auth=user, product_id=pk_product)
            like.save()

        return redirect('home_page')


def download_file(request, slug_path):
    game = get_object_or_404(Products, slug=slug_path)
    if game.file_came:
        response = FileResponse(open(game.file_came.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{game.file_came.name}"'
        return response
    else:
        success(request, 'Нету файла игры (((')
        return redirect('detail', game.slug)
