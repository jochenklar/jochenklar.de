# Generated by Django 2.1.4 on 2019-01-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_add_color_red_green_blue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='blue',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='color',
            name='green',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='color',
            name='red',
            field=models.IntegerField(default=0),
        ),
    ]
