from django import template
from pages.models import Favorite
register = template.Library()


@register.simple_tag()
def check_favorite(user, game_id):
    return Favorite.objects.filter(auth=user, game_id=game_id).exists()
