# Generated by Django 2.1.4 on 2019-01-15 10:21

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_projectpage_references'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpage',
            name='references_de',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
