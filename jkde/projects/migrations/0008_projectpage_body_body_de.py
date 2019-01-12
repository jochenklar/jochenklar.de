# Generated by Django 2.1.4 on 2019-01-12 12:24

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_rename_body_to_teaser'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpage',
            name='body',
            field=wagtail.core.fields.StreamField([('richtext', wagtail.core.blocks.RichTextBlock()), ('html', wagtail.core.blocks.RawHTMLBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True),
        ),
        migrations.AddField(
            model_name='projectpage',
            name='body_de',
            field=wagtail.core.fields.StreamField([('richtext', wagtail.core.blocks.RichTextBlock()), ('html', wagtail.core.blocks.RawHTMLBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True),
        ),
    ]
