# Generated by Django 3.2.4 on 2023-01-12 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StockList',
            new_name='CoinData',
        ),
    ]
