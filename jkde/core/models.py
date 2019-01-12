from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from jkde.core.fields import TranslatedTitleField, TranslatedTextField


class SingletonMixin(object):

    @classmethod
    def can_create_at(cls, parent):
        # Only create one Singleton
        return super().can_create_at(parent) and not cls.objects.exists()


class PaginatorMixin(RoutablePageMixin):

    pagination_order = '-first_published_at'
    page_size = 5

    def get_context(self, request, page=1):
        context = super().get_context(request)

        queryset = self.get_children().live().order_by(self.pagination_order)
        paginator = Paginator(queryset, self.page_size)

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


class HomePage(SingletonMixin, Page):

    title_de = models.CharField(max_length=255, blank=True)

    body = RichTextField(blank=True)
    body_de = RichTextField(blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    image_credit = RichTextField(blank=True)

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
        FieldPanel('image_credit', classname='full'),
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

    image_credit = RichTextField(blank=True)

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
        FieldPanel('image_credit', classname='full'),
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

    name = models.CharField(max_length=255)
    red = models.IntegerField(default=0)
    green = models.IntegerField(default=0)
    blue = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('red'),
        FieldPanel('green'),
        FieldPanel('blue')
    ]

    @property
    def style(self):
        return '''
        <style>
            a, a:hover, a:focus, a:visited {
                color: rgb(%(red)s, %(green)s, %(blue)s);
            }
            blockquote p,
            address,
            pre {
                border-color: rgb(%(red)s, %(green)s, %(blue)s);
                background-color: rgb(%(red)s, %(green)s, %(blue)s, 0.1);
            }
        </style>
        ''' % {
            'red': self.red,
            'green': self.green,
            'blue': self.blue
        }
