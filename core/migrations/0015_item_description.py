# Generated by Django 3.0.5 on 2020-04-19 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_item_isnewitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='This is a Fake Description'),
        ),
    ]
