from django.http import FileResponse
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import ReviewForm
from account.models import Profile
from payment.models import GameLibrary
from .models import Categories, Games, Favorite, Review, Rating, ViewsGame


def index_page(request):
    categories = Categories.objects.all()
    games = Games.objects.filter(discount=0)

    games_discount = [i for i in Games.objects.all() if i.discount > 0]

    content = {
        'active': 1,
        'categories': categories,
        'games': games[3:7][::-1],
        'games_discount': games_discount[:3]
    }
    return render(request, 'pages/index.html', context=content)


class CatalogPage(ListView):
    model = Games
    template_name = 'pages/catalog.html'
    context_object_name = 'games'
    paginate_by = 4
    extra_context = {
        'active': 2,
        'categories': Categories.objects.all()
    }


class ShowGameRelatedCategories(CatalogPage):
    def get_queryset(self):
        games = Games.objects.filter(category_id=self.kwargs['cat_id'])
        return games

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = Categories.objects.get(pk=self.kwargs['cat_id'])
        return context


class SearchGameToTitle(CatalogPage):
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Games.objects.filter(
            Q(title__iregex=query) | Q(title__icontains=query)
        )


def show_detail(request, slug_path):
    game = get_object_or_404(Games, slug=slug_path)

    comments = game.comments.filter(parent=None)
    if request.method == "POST":
        comment_form = ReviewForm(data=request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.auth = request.user
            comment_form.game = game
            comment_form.save()
            return redirect('detail_path', game.slug)
        else:
            messages.warning(request, 'Что то пошло не так')
            return redirect('detail_path', game.slug)

    else:
        comment_form = ReviewForm()

    if request.user.is_authenticated:
        if not request.session.session_key:
            request.session.save()

        session_key = request.session.session_key
        status_view = ViewsGame.objects.filter(game=game, user_session=session_key).exists()
        if status_view is False and session_key != 'None':
            view = ViewsGame()
            view.game = game
            view.user_session = session_key
            view.save()
            game.views += 1
            game.save()

    content = {
        'game': game,
        'comments': comments,
        'comment_form': comment_form,
        'range_number': [num for num in range(1, 6)][::-1]
    }
    return render(request, 'pages/detail.html', content)


# {% for num in  %}
#
#
#                                 {% endfor %}
#                                 <button type="submit" class="btn btn-danger">Оценить</button>

def add_reply(request, pk):
    comment = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        comment_form = ReviewForm(data=request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.auth = request.user
            comment_form.game = comment.game
            comment_form.parent = comment
            comment_form.save()
            return redirect('detail_path', comment.game.slug)
        else:
            messages.warning(request, 'Что то пошло не так')
            return redirect('detail_path', comment.game.slug)
    else:
        comment_form = ReviewForm()

    content = {
        'comment_form': comment_form
    }
    return render(request, 'pages/detail.html', content)


def like_logic(request, pk_game):
    if request.user.is_authenticated:
        user = request.user
        status = Favorite.objects.filter(auth=user, game_id=pk_game).exists()
        if status:
            like = Favorite.objects.get(auth=user, game_id=pk_game)
            like.delete()
        else:
            like = Favorite.objects.create(auth=user, game_id=pk_game)
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
    game = get_object_or_404(Games, slug=slug_path)
    if game.file_came:
        response = FileResponse(open(game.file_came.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{game.file_came.name}"'
        return response
    else:
        messages.error(request, 'Нету файла игры (((')
        return redirect(request.META.get('HTTP_REFERER', 'home_path'))


def rating_logic(request, pk_path):
    if request.user.is_authenticated:
        user = request.user
        game = get_object_or_404(Games, pk=pk_path)
        status = Rating.objects.filter(user_id=user.pk, game_id=game.pk).exists()
        if status is False:
            if request.method == 'GET':
                int_rating = request.GET.get('stars')
                rating = Rating.objects.create(user=user, game=game, quantity_star=int_rating)
                rating.save()
                return redirect('detail_path', game.slug)
        else:
            messages.error(request, 'Вы не можете оценить одну и тужу игру')
            return redirect(request.META.get('HTTP_REFERER', 'home_path'))
    else:
        messages.error(request, 'Вы не вошли в аккаунт, поэтому вы не можете оценить игру')
        return redirect(request.META.get('HTTP_REFERER', 'home_path'))

