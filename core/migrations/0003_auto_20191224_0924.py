# Generated by Django 3.0.1 on 2019-12-24 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191224_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default=False, height_field=295.45, upload_to='', width_field=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shirt'), ('SP', 'Sports'), ('W', 'Winter'), ('P', 'Party Wear'), ('F', 'Formals'), ('C', 'Casuals')], max_length=2),
        ),
    ]
