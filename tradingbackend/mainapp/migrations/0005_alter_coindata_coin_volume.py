# Generated by Django 3.2.4 on 2023-01-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_coindata_coin_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coindata',
            name='coin_volume',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
