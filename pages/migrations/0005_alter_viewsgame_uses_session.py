# Generated by Django 5.0.6 on 2024-07-23 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_rename_file_came_games_file_game_games_views_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewsgame',
            name='uses_session',
            field=models.CharField(max_length=150),
        ),
    ]