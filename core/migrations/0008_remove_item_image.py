# Generated by Django 3.0.1 on 2019-12-24 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
    ]
