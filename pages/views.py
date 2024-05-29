from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success
from django.http import FileResponse
from django.views.generic import ListView

from .models import Categories, Products, Favorite, Review
from .forms import ReviewForm


def index_page(request):
    categories = Categories.objects.all()
    games = Products.objects.all()
    games_discount = [i for i in games if i.discount > 0]
    content = {
        'categories': categories,
        'games': games[2:5][::-1],
        'games_discount': games_discount
    }
    return render(request, 'index.html', context=content)


def show_game_by_cat_id(request, cat_id):
    games = Products.objects.filter(category_id=cat_id)
    categories = Categories.objects.all()
    content = {
        'games': games,
        'categories': categories
    }
    return render(request, 'index.html', content)


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
            return redirect('detail', game.slug)
    else:
        comment_form = ReviewForm()

    content = {
        'game': game,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'detail.html', content)


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
        status = Favorite.objects.filter(auth=user, product_id=pk_product).exists()
        if status:
            like = Favorite.objects.get(auth=user, product_id=pk_product)
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


class CatalogPage(ListView):
    model = Products
    template_name = 'catalog.html'
    context_object_name = 'games'
    paginate_by = 3
    extra_context = {
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
