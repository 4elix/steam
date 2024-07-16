from django.shortcuts import redirect
from django.contrib import messages

from .models import Products, OrderProduct, Order, Customer


class CartForAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user
        self.request = request
        if product_id and action:
            self.add_or_delete(product_id, action)

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
            'products': order_product
        }
        return context

    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()['order']
        product = Products.objects.get(pk=product_id)
        print(product.pk)

        order_product = OrderProduct.objects.filter(order=order, product_id=product.pk).exists()
        if order_product is False:
            create_order_product = OrderProduct.objects.create(order=order, product=product)
            if action == 'add':
                create_order_product.quantity += 1
            else:
                create_order_product.quantity -= 1

            create_order_product.save()

            if create_order_product.quantity <= 0:
                create_order_product.delete()
        else:
            return 404

    def clear(self):
        order = self.get_cart_info()['order']
        order_product = order.orderproduct_set.all()
        for product in order_product:
            product.delete()
        order.save()


def get_cart_data(request):
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()
    context = {
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'products': cart_info['products']
    }
    return context
