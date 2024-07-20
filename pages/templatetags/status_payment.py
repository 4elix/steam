from django import template
from payment.models import GameLibrary

register = template.Library()


@register.simple_tag()
def check_payment(user, game_id):
    return GameLibrary.objects.filter(user=user, game_id=game_id).exists()
