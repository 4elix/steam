from django.http import FileResponse
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import ReviewForm
from account.models import Profile
from payment.models import GameLibrary
from .models import Categories, Products, Favorite, Review


def index_page(request):
    categories = Categories.objects.all()
    games = Products.objects.all()
    games_discount = [i for i in games if i.discount > 0]

    content = {
        'active': 1,
        'categories': categories,
        'games': games[2:5][::-1],
        'games_discount': games_discount
    }
    return render(request, 'pages/index.html', context=content)


class CatalogPage(ListView):
    model = Products
    template_name = 'pages/catalog.html'
    context_object_name = 'games'
    paginate_by = 3
    extra_context = {
        'active': 2,
        'categories': Categories.objects.all()
    }


class ShowGameRelatedCategories(CatalogPage):
    def get_queryset(self):
        games = Products.objects.filter(category_id=self.kwargs['cat_id'])
        return games

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = Categories.objects.get(pk=self.kwargs['cat_id'])
        return context


class SearchGameToTitle(CatalogPage):
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Products.objects.filter(
            Q(title__iregex=query) | Q(title__icontains=query)
        )


def show_detail(request, slug_path):
    game = get_object_or_404(Products, slug=slug_path)

    comments = game.comments.filter(parent=None)
    if request.method == "POST":
        comment_form = ReviewForm(data=request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.auth = request.user
            comment_form.product = game
            comment_form.save()
        else:
            messages.warning(request, 'Что то пошло не так')
            return redirect('detail_path', game.slug)

    else:
        comment_form = ReviewForm()

    content = {
        'game': game,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'pages/detail.html', content)


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
        else:
            messages.warning(request, 'Что то пошло не так')
            return redirect('detail_path', comment.product.slug)
    else:
        comment_form = ReviewForm()

    content = {
        'comment_form': comment_form
    }
    return render(request, 'pages/detail.html', content)


def like_logic(request, pk_product):
    if request.user.is_authenticated:
        user = request.user
        status = Favorite.objects.filter(auth=user, product_id=pk_product).exists()
        if status:
            like = Favorite.objects.get(auth=user, product_id=pk_product)
            like.delete()
        else:
            like = Favorite.objects.create(auth=user, product_id=pk_product)
            like.save()

        return redirect(request.META.get('HTTP_REFERER', 'home_path'))


def page_desired(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    list_desired = Favorite.objects.filter(auth=profile.user)
    list_comment = Review.objects.filter(auth=profile.user)
    list_buy_game = GameLibrary.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'list_desired': list_desired,
        'count_user_desired': list_desired.count(),
        'count_user_reviews': list_comment.count(),
        'count_user_buy_game': list_buy_game.count(),
        'user_name': request.user.username,
        'active': 4
    }
    return render(request, 'pages/desired.html', context)


def download_file(request, slug_path):
    game = get_object_or_404(Products, slug=slug_path)
    if game.file_came:
        response = FileResponse(open(game.file_came.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{game.file_came.name}"'
        return response
    else:
        messages.error(request, 'Нету файла игры (((')
        return redirect(request.META.get('HTTP_REFERER', 'home_path'))
