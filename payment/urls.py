from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('to_cart/<int:game_id>/<str:action>/', views.to_cart, name='to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.create_checkout_session, name='payment'),
    path('success/', views.success_payment, name='success'),
    path('clear_cart/', views.clear_card, name='clear_cart'),
    path('game/library/', views.show_library, name='game_library')
]
