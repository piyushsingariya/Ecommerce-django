# Generated by Django 3.0.1 on 2019-12-24 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='previous_price',
            field=models.FloatField(default=0),
        ),
    ]
