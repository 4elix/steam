from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')

    price_old = models.FloatField(default=0, blank=True, null=True)
    price_new = models.FloatField(default=0, blank=True, null=True)
    discount = models.FloatField(default=0, blank=True, null=True)

    limitation_age = models.IntegerField(default=18)
    date_time = models.DateTimeField(auto_now=False, blank=True, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(max_length=200, blank=True, null=True)
    tags = models.ManyToManyField('TagsGame', related_name='tag_game', verbose_name='Теги или под категории для игры')
    file_came = models.FileField(upload_to='game/file/', verbose_name='Файлы для скачки', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_first_photo(self):
        photo = self.game_photo.all().first()
        if photo is not None:
            return photo.photo.url
        return "https://images.satu.kz/126101312_w640_h640_razdel-v-razrabotketovary.jpg"

    def get_second_photo(self):
        try:
            photo = self.game_photo.all()[1:]
            if photo is not None:
                return photo
        except:
            return "https://images.satu.kz/126101312_w640_h640_razdel-v-razrabotketovary.jpg"

    class Meta:
        # verbose_name -> задает имя в админ панельке
        verbose_name = 'Игра'
        # verbose_name_plural -> задает имя в админ панельке во множественном числе
        verbose_name_plural = 'Игры'


class TagsGame(models.Model):
    tag_name = models.CharField(max_length=200, verbose_name='Теги или под категории')

    def __str__(self):
        return self.tag_name


class Review(models.Model):
    datetime_review = models.DateTimeField(auto_now=True, verbose_name='Дата и время создания комментария')
    auth = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(verbose_name='Комментарий')
    product = models.ForeignKey(Products, on_delete=models.CASCADE,
                                verbose_name='К какому продукты отставлен комментарий', related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.datetime_review}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Favorite(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


class ProductImage(models.Model):
    photo = models.ImageField(verbose_name="Фото", upload_to="products/", blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='game_photo')


