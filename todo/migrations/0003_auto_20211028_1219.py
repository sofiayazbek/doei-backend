# Generated by Django 3.1.5 on 2021-10-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20211025_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(verbose_name='Total')),
                ('data', models.DateField(verbose_name='Data de entrega para a Instituição')),
            ],
            options={
                'verbose_name': 'Cesta',
                'verbose_name_plural': 'Cestas',
            },
        ),
        migrations.AlterField(
            model_name='instituicao',
            name='descricao',
            field=models.CharField(max_length=500, verbose_name='Descrição'),
        ),
    ]
