# Generated by Django 3.2.3 on 2024-03-19 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20240311_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-recipe__pub_date'], 'verbose_name': 'Избранный рецепт пользователей', 'verbose_name_plural': 'Избранные рецепты пользователей'},
        ),
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'ordering': ['-recipe__pub_date'], 'verbose_name': 'Список покупок пользователей', 'verbose_name_plural': 'Списки покупок пользователей'},
        ),
        migrations.AlterModelOptions(
            name='subscribe',
            options={'ordering': ['author__username'], 'verbose_name': 'Подписки пользователей', 'verbose_name_plural': 'Подписки пользователей'},
        ),
    ]