# Generated by Django 2.1.4 on 2019-01-14 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_projectpage_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectpagecollaboration',
            name='page',
        ),
        migrations.RemoveField(
            model_name='projectpagerelatedlink',
            name='page',
        ),
        migrations.DeleteModel(
            name='ProjectPageCollaboration',
        ),
        migrations.DeleteModel(
            name='ProjectPageRelatedLink',
        ),
    ]