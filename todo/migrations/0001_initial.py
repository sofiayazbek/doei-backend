# Generated by Django 3.1.5 on 2021-10-18 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Filme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField()),
                ('sinopse', models.TextField()),
                ('duracao', models.IntegerField()),
                ('atores', models.ManyToManyField(to='todo.Ator')),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.TextField()),
                ('capacidade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TodoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sessao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('filme', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='todo.filme')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='todo.sala')),
            ],
        ),
    ]
