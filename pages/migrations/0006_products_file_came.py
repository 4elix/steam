# Generated by Django 5.0.6 on 2024-05-26 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_review_parent_alter_review_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='file_came',
            field=models.FileField(blank=True, null=True, upload_to='game/file/', verbose_name='Файлы для скачки'),
        ),
    ]
