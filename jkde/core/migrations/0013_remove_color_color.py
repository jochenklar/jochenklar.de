# Generated by Django 2.1.4 on 2019-01-07 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_homepage_image_credit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='color',
        ),
    ]
