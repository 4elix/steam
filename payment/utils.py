from django.shortcuts import redirect
from django.contrib import messages

from .models import Games, OrderProduct, Order, Customer


class CartForAuthenticatedUser:
    def __init__(self, request, game_id=None, action=None):
        self.user = request.user
        self.request = request
        if game_id and action:
            self.add_or_delete(game_id, action)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user)
        order, created = Order.objects.get_or_create(customer=customer)
        order_product = order.orderproduct_set.all()

        cart_total_price = order.get_cart_total_price
        cart_total_quantity = order.get_cart_total_quantity
        context = {
            'cart_total_price': cart_total_price,
            'cart_total_quantity': cart_total_quantity,
            'order': order,
            'games': order_product
        }
        return context

    def add_or_delete(self, game_id, action):
        order = self.get_cart_info()['order']
        game = Games.objects.get(pk=game_id)
        create_order_product = OrderProduct.objects.create(order=order, game=game)
        if action == 'add':
            create_order_product.quantity += 1
        else:
            create_order_product.quantity -= 1

        create_order_product.save()

        if create_order_product.quantity <= 0:
            create_order_product.delete()

    def check_game_order_product(self, game_id, order):
        status = OrderProduct.objects.filter(order=order, game_id=game_id).exists()
        return status

    def clear(self):
        order = self.get_cart_info()['order']
        order_product = order.orderproduct_set.all()
        for game in order_product:
            game.delete()
        order.save()


def get_cart_data(request):
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()
    context = {
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'games': cart_info['games']
    }
    return context
