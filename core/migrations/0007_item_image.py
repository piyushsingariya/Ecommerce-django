# Generated by Django 3.0.1 on 2019-12-24 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
