# Generated by Django 3.1.5 on 2021-11-04 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20211028_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituicao',
            name='produtos',
            field=models.ManyToManyField(to='todo.Produto', verbose_name='Produtos'),
        ),
    ]
