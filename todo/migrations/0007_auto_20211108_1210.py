# Generated by Django 3.1.5 on 2021-11-08 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_contato'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assunto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Assunto',
                'verbose_name_plural': 'Assuntos',
            },
        ),
        migrations.AddField(
            model_name='contato',
            name='assunto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='todo.assunto', verbose_name='Assunto'),
        ),
    ]
