from django.db import models
from django.contrib.auth.models import User
from pages.models import Games


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=250, default='', verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=250, default='', verbose_name='Фамилия покупателя')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Заказ выполнен')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        order_product = self.orderproduct_set.all()  # получаем заказанные продукты самого заказа
        total_price = sum([games.get_total_price for games in order_product])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_product = self.orderproduct_set.all()  # получаем заказанные продукты самого заказа
        total_quantity = sum([games.quantity for games in order_product])
        return total_quantity


class OrderProduct(models.Model):
    game = models.ForeignKey(Games, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'продукт в заказе'
        verbose_name_plural = 'продукты в заказе'

    # Метод который вернет сумму товара в его кол-ве
    @property  # декоратор нужен что-бы было вызывать метод в другой модели
    def get_total_price(self):
        if self.game.price_new == 0:
            total_price = self.game.price_old * self.quantity
        else:
            total_price = self.game.price_new * self.quantity

        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=300, verbose_name='Адрес (ул, дом, кв)')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    region = models.CharField(max_length=200, verbose_name='Регион')
    phone = models.CharField(max_length=200, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата доставки')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class City(models.Model):
    city_name = models.CharField(max_length=300, verbose_name='Город')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class GameLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='library_game')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Библиотека игр'
        verbose_name_plural = 'Библиотеки игр'
