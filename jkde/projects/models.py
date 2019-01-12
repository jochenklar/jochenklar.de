from django.db import models
from django.utils.translation import ugettext_lazy as _

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
from jkde.core.fields import TranslatedTitleField, TranslatedTextField, TranslatedStreamField


class ProjectIndexPage(SingletonMixin, PaginatorMixin, Page):

    title_de = models.CharField(max_length=255, blank=True)

    intro = RichTextField(blank=True)
    intro_de = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    image_credit = RichTextField(blank=True)

    color = models.ForeignKey(
        'core.Color', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    trans_title = TranslatedTitleField('title')
    trans_intro = TranslatedTextField('intro')

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname='full'),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('intro_de', classname='full'),
    ]
    misc_panels = [
        ImageChooserPanel('image'),
        FieldPanel('image_credit', classname='full'),
        SnippetChooserPanel('color'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_de_panels, heading='Content DE'),
        ObjectList(misc_panels, heading='Misc'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    subpage_types = ['projects.ProjectPage']

    pagination_order = '-projectpage__start_date'
    page_size = 10


class ProjectPage(Page):

    title_de = models.CharField(max_length=255, blank=True)

    subtitle = models.CharField(max_length=255, blank=True)
    subtitle_de = models.CharField(max_length=255, blank=True)

    teaser = RichTextField(blank=True)
    teaser_de = RichTextField(blank=True)

    BODY_BLOCKS = [
        ('richtext', RichTextBlock()),
        ('html', RawHTMLBlock()),
        ('image', ImageChooserBlock()),
    ]

    body = StreamField(BODY_BLOCKS, blank=True)
    body_de = StreamField(BODY_BLOCKS, blank=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, _('in progress')),
        (STATUS_COMPLETED, _('completed'))
    )

    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)

    trans_title = TranslatedTitleField('title')
    trans_subtitle = TranslatedTitleField('subtitle')
    trans_teaser = TranslatedTitleField('teaser')
    trans_body = TranslatedStreamField('body')

    search_fields = Page.search_fields + [
        index.SearchField('title_de'),
        index.SearchField('subtitle'),
        index.SearchField('subtitle_de'),
        index.SearchField('teaser'),
        index.SearchField('teaser_de'),
        index.SearchField('body'),
        index.SearchField('body_de'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('subtitle', classname="full title"),
        FieldPanel('teaser', classname='full'),
        StreamFieldPanel('body', classname='full'),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('subtitle_de', classname="full title"),
        FieldPanel('teaser_de', classname='full'),
        StreamFieldPanel('body_de', classname='full'),
    ]
    misc_panels = [
        FieldPanel('status'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        InlinePanel('collaborations', label='Collaborations'),
        InlinePanel('related_links', label='Related links'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_de_panels, heading='Content DE'),
        ObjectList(misc_panels, heading='Misc'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname='settings'),
    ])

    parent_page_types = ['projects.ProjectIndexPage']

    @property
    def color(self):
        return self.get_parent().specific.color


class ProjectPageCollaboration(Orderable):

    page = ParentalKey('projects.ProjectPage', on_delete=models.CASCADE, related_name='collaborations')

    name = models.CharField(max_length=255)
    url = models.URLField('External link', blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class ProjectPageRelatedLink(Orderable):

    page = ParentalKey('projects.ProjectPage', on_delete=models.CASCADE, related_name='related_links')

    title = models.CharField(max_length=255)
    url = models.URLField('External link', blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('url'),
    ]
