# Generated by Django 4.2.13 on 2024-06-04 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_alter_tagsgame_options_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]