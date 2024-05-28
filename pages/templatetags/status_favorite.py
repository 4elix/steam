from django import template
from pages.models import Favorite
register = template.Library()


@register.simple_tag()
def check_favorite(user, product_id):
    return Favorite.objects.filter(auth=user, product_id=product_id).exists()
