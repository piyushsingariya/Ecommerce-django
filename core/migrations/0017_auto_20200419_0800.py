# Generated by Django 3.0.5 on 2020-04-19 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_item_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
