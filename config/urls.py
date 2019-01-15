from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from jkde.core import views as core_views


urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    re_path(r'i18n/([a-z]{2})/$', core_views.i18n_switcher, name='i18n_switcher'),

    path('', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = TemplateView.as_view(template_name='core/400.html')
handler403 = TemplateView.as_view(template_name='core/403.html')
handler404 = TemplateView.as_view(template_name='core/404.html')
handler500 = TemplateView.as_view(template_name='core/500.html')
