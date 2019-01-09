from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from jkde.core.models import SingletonMixin
from jkde.core.fields import TranslatedTitleField, TranslatedTextField


class BlogIndexPage(SingletonMixin, RoutablePageMixin, Page):

    title_de = models.CharField(max_length=255, blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    image_credit = RichTextField(blank=True)

    color = models.ForeignKey(
        'core.Color', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    trans_title = TranslatedTitleField('title')
    trans_intro = TranslatedTextField('intro')

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

    def get_context(self, request, page=1):
        context = super().get_context(request)

        queryset = self.get_children().live().order_by('-first_published_at')
        paginator = Paginator(queryset, 5)

        try:
            context['paginator'] = paginator.page(page)
        except PageNotAnInteger:
            context['paginator'] = paginator.page(1)
        except EmptyPage:
            context['paginator'] = paginator.page(paginator.num_pages)

        return context

    @route(r'^page/(\d+)/$', name='pagination')
    def pagination_route(self, request, page):
        return self.index_route(request, page)


class BlogPage(Page):

    title_de = models.CharField(max_length=255, blank=True)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    trans_title = TranslatedTitleField('title')
    trans_body = TranslatedTextField('body')

    search_fields = Page.search_fields + [
        index.SearchField('title_de'),
        index.SearchField('body'),
        index.SearchField('body_de'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname='full'),
    ]
    content_de_panels = [
        FieldPanel('title_de', classname="full title"),
        FieldPanel('body_de', classname='full'),
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
