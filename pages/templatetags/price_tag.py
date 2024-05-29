import random
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def price_simple_tag(price_old, price_new, discount):
    if discount == 0.0 and price_new == 0.0:
        part_dont_discount = f'<p class="fs-5 my-auto text-blueviolet">{price_old} $$</p>'
        return mark_safe(part_dont_discount)
    elif price_old < price_new:
        part_price_new = f'''
<div class="d-flex flex-column pb-2 text-blueviolet">
<p class="my-auto text-warning text-decoration-line-through">{price_old} $$</p>
<p class="my-auto text-danger fs-5">{price_new} $$</p>
</div>
'''
        return mark_safe(part_price_new)
    else:
        part_discount = f'''
<div class="d-flex flex-column pb-2 text-blueviolet">
<p class="my-auto text-warning text-decoration-line-through">{price_old} $$</p>
<p class="my-auto text-danger fs-5">{price_new} $$</p>
<p class="my-auto text-danger fs-5">{discount} %</p>
</div>
'''
        return mark_safe(part_discount)
