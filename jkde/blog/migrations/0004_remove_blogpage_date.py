# Generated by Django 2.1.4 on 2019-01-09 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_blogindexpage_intro_de'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='date',
        ),
    ]