from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    TabbedInterface,
    ObjectList
)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.search import index

from wagtail.snippets.edit_handlers import SnippetChooserPanel

from jkde.core.models import SingletonMixin
from jkde.core.fields import TranslatedTitleField, TranslatedTextField


class ProjectIndexPage(SingletonMixin, Page):

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

    subpage_types = ['projects.ProjectPage']


class ProjectPage(Page):

    title_de = models.CharField(max_length=255, blank=True)

    subtitle = models.CharField(max_length=255, blank=True)
    subtitle_de = models.CharField(max_length=255, blank=True)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    trans_title = TranslatedTitleField('title')
    trans_subtitle = TranslatedTitleField('subtitle')
    trans_body = TranslatedTextField('body')

    search_fields = Page.search_fields + [
        index.SearchField('title_de'),
        index.SearchField('body'),
        index.SearchField('body_de'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('subtitle', classname="full title"),
        FieldPanel('body', classname='full'),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('subtitle_de', classname="full title"),
        FieldPanel('body_de', classname='full'),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel('start_date'),
        FieldPanel('end_date'),
        InlinePanel('collaborations', label='Collaborations'),
        InlinePanel('related_links', label='Related links'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_de_panels, heading='Content DE'),
        ObjectList(promote_panels, heading='Promote'),
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
