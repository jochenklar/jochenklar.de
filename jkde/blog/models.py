from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock, RawHTMLBlock

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    InlinePanel,
    TabbedInterface,
    ObjectList
)

from wagtail.search import index

from wagtail.snippets.edit_handlers import SnippetChooserPanel

from jkde.core.models import SingletonMixin, PaginatorMixin
from jkde.core.fields import TranslatedTextField, TranslatedStreamField


class BlogIndexPage(SingletonMixin, PaginatorMixin, Page):

    title_de = models.CharField(max_length=255, blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    image_credit = RichTextField(blank=True)

    color = models.ForeignKey(
        'core.Color', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    trans_title = TranslatedTextField('title')
    trans_intro = TranslatedTextField('intro', note=True)

    content_panels = [
        FieldPanel('title', classname="full title"),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
    ]
    promote_panels = Page.promote_panels + [
        ImageChooserPanel('image'),
        FieldPanel('image_credit', classname='full'),
        SnippetChooserPanel('color'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_de_panels, heading='Content DE'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    subpage_types = ['blog.BlogPage']


class BlogPage(Page):

    title_de = models.CharField(max_length=255, blank=True)

    BODY_BLOCKS = [
        ('richtext', RichTextBlock()),
        ('html', RawHTMLBlock()),
        ('image', ImageChooserBlock()),
    ]

    body = StreamField(BODY_BLOCKS, blank=True)
    body_de = StreamField(BODY_BLOCKS, blank=True)

    trans_title = TranslatedTextField('title')
    trans_body = TranslatedStreamField('body')

    search_fields = Page.search_fields + [
        index.SearchField('title_de'),
        index.SearchField('body'),
        index.SearchField('body_de'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel('body'),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
        StreamFieldPanel('body_de'),
    ]
    promote_panels = Page.promote_panels + [
        InlinePanel('related_links', label='Related links'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_de_panels, heading='Content DE'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])

    parent_page_types = ['blog.BlogIndexPage']

    @property
    def color(self):
        return self.get_parent().specific.color


class BlogPageRelatedLink(Orderable):

    page = ParentalKey('blog.BlogPage', on_delete=models.CASCADE, related_name='related_links')

    title = models.CharField(max_length=255)
    url = models.URLField('External link', blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('url'),
    ]
