from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, unique=False,
                                verbose_name='Профиль которая привязывает пользователя')

    profile_image = models.ImageField(upload_to='profile/image_account/', null=True, blank=True,
                                      verbose_name='Аватарка пользователя')

    first_name = models.CharField(max_length=200, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия', null=True, blank=True)
    phone = models.CharField(max_length=200, verbose_name='Телефон', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} --- {self.last_name} --- {self.phone}'


