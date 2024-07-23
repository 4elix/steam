from django import template
from django.shortcuts import get_object_or_404

from pages.models import Rating

register = template.Library()


@register.simple_tag()
def show_rating(user, game_id):
    status = Rating.objects.filter(user_id=user.pk, game_id=game_id).exists()
    if status:
        rating = Rating.objects.get(game_id=game_id, user_id=user.pk)
        try:
            rating_all = Rating.objects.get(game_id=game_id)
            total_quantity = len(rating_all)
            total_sum = sum([item.quantity_star for item in rating_all])
            overall_rating = total_sum / total_quantity
            return {
                'rating': rating,
                'overall_rating': overall_rating
            }
        except:
            return {
                'rating': rating,
                'overall_rating': 0
            }
    else:
        try:
            rating_all = Rating.objects.get(game_id=game_id)
            total_quantity = len(rating_all)
            total_sum = sum([item.quantity_star for item in rating_all])
            overall_rating = total_sum / total_quantity
            return {
                'status': 'show_form',
                'overall_rating': overall_rating
            }
        except:
            return {
                'status': 'show_form',
                'overall_rating': 0
            }
