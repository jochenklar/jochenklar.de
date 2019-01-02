from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    PageChooserPanel,
    TabbedInterface,
    ObjectList
)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from jkde.core.fields import TranslatedTitleField, TranslatedTextField


class SingletonMixin(object):

    @classmethod
    def can_create_at(cls, parent):
        # Only create one Singleton
        return super().can_create_at(parent) and not cls.objects.exists()


class HomePage(SingletonMixin, Page):

    title_de = models.CharField(max_length=255, blank=True)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    color = models.ForeignKey(
        'core.Color', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    trans_title = TranslatedTitleField('title')
    trans_body = TranslatedTextField('body')

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname='full'),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('body_de', classname='full'),
    ]
    promote_panels = Page.promote_panels + [
        ImageChooserPanel('image'),
        SnippetChooserPanel('color'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_de_panels, heading='Content DE'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class MainPage(Page):

    title_de = models.CharField(max_length=255, blank=True)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    color = models.ForeignKey(
        'core.Color', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    trans_title = TranslatedTitleField('title')
    trans_body = TranslatedTextField('body')

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname='full'),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('body_de', classname='full'),
    ]
    promote_panels = Page.promote_panels + [
        ImageChooserPanel('image'),
        SnippetChooserPanel('color'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_de_panels, heading='Content DE'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class TextPage(Page):

    title_de = models.CharField(max_length=255, null=False, blank=False)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    color = models.ForeignKey(
        'core.Color', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    trans_title = TranslatedTitleField('title')
    trans_body = TranslatedTextField('body')

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname='full'),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('body_de', classname='full'),
    ]
    promote_panels = Page.promote_panels + [
        SnippetChooserPanel('color'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_de_panels, heading='Content DE'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


@register_setting
class Settings(BaseSetting):

    header_navigation = models.ForeignKey(
        'core.Menu', null=True, on_delete=models.SET_NULL, related_name='+')

    footer_navigation = models.ForeignKey(
        'core.Menu', null=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        SnippetChooserPanel('header_navigation'),
        SnippetChooserPanel('footer_navigation')
    ]


@register_snippet
class Menu(ClusterableModel):

    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        InlinePanel('items', label='Pages'),
    ]


class MenuItem(Orderable):
    parent = ParentalKey('core.Menu', related_name='items')
    page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        PageChooserPanel('page'),
    ]


@register_snippet
class Color(ClusterableModel):

    name = models.CharField(max_length=255, null=False, blank=False)
    color = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('color'),
    ]

    @property
    def style(self):
        return '<style>a, a:hover, a:focus, a:visited { color: %s }</style>' % self.color
