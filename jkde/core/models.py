from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from jkde.core.fields import TranslatedTitleField, TranslatedTextField


class SingletonMixin(object):

    @classmethod
    def can_create_at(cls, parent):
        # Only create one ProjectIndexPage
        return super().can_create_at(parent) and not cls.objects.exists()


class HomePage(SingletonMixin, Page):

    title_de = models.CharField(max_length=255, blank=True)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    trans_title = TranslatedTitleField('title')
    trans_body = TranslatedTextField('body')

    content_panels = Page.content_panels + [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('body', classname='full'),
        FieldPanel('body_de', classname='full'),
        ImageChooserPanel('image'),
    ]


class MainPage(Page):

    title_de = models.CharField(max_length=255, blank=True)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    trans_title = TranslatedTitleField('title')
    trans_body = TranslatedTextField('body')

    content_panels = Page.content_panels + [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('body', classname='full'),
        FieldPanel('body_de', classname='full'),
        ImageChooserPanel('image'),
    ]


class TextPage(Page):

    title_de = models.CharField(max_length=255, null=False, blank=False)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    trans_title = TranslatedTitleField('title')
    trans_body = TranslatedTextField('body')

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('title_de', classname="full title"),
        FieldPanel('body', classname='full'),
        FieldPanel('body_de', classname='full'),
    ]
