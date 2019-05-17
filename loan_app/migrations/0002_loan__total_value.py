# Generated by Django 2.2.1 on 2019-05-15 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='_total_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='total value'),
            preserve_default=False,
        ),
    ]