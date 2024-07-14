import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .models import Customer
from .forms import CustomerForm, ShippingForm
from .utils import get_cart_data, CartForAuthenticatedUser


def cart(request):
    cart_info = get_cart_data(request)

    context = {
        'title': 'Моя корзина',
        'order': cart_info['order'],
        'products': cart_info['products'],
    }
    return render(request, 'payment/cart.html', context)


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
        messages.success(request, 'Все готово')
        page = request.META.get('HTTP_REFERER', 'product_list')
        return redirect(page)
    else:
        page = request.META.get('HTTP_REFERER', 'product_list')
        messages.success(request, 'Все готово')
        return redirect(page)


def checkout(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Оформления заказа',
            'order': cart_info['order'],
            'items': cart_info['products'],
            'shipping_form': ShippingForm(),
            'customer_form': CustomerForm()
        }
        return render(request, 'payment/checkout.html', context)


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)  # Получ корзину покупателя
        cart_info = user_cart.get_cart_info()  # Из корзины при помощи метода получаем информацию о корзине

        # Сохранение данных покупателя
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)  # Получиди покупателя по пользователю
            customer.first_name = customer_form.cleaned_data['first_name']  # Указали имя покупателю по данным из формы
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.save()

        # Сохранение данных Адреса доставки
        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()

        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Покупка на сайте STEAM-TEST'
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )

        return redirect(session.url, 303)


def success_payment(request):
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    messages.success(request, 'Ваша оплата прошла успешно')
    return render(request, 'payment/success.html')


def clear_card(request):
    user_cart = CartForAuthenticatedUser(request)
    order = user_cart.get_cart_info()['order']
    order_products = order.orderproduct_set.all()
    for order_product in order_products:
        order_product.delete()

    return redirect('cart')
