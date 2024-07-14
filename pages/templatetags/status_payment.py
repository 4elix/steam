from django import template
from payment.models import GameLibrary

register = template.Library()


@register.simple_tag()
def check_payment(user, product_id):
    return GameLibrary.objects.filter(user=user, product_id=product_id).exists()
