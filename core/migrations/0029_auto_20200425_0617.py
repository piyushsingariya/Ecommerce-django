# Generated by Django 3.0.5 on 2020-04-25 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20200425_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default=0, max_length=30),
        ),
    ]
