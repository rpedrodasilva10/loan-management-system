# Generated by Django 2.2.1 on 2019-05-11 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('active', models.BooleanField(default=True, verbose_name='Ativo: ')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Atualizado em: ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em: ')),
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=11)),
                ('cpf', models.CharField(max_length=11, unique=True, verbose_name='CPF')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
    ]
