# Generated by Django 3.2.3 on 2024-03-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_auto_20240314_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipe.Tag', verbose_name='Тэги'),
        ),
    ]
