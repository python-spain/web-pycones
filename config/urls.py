# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views import defaults as default_views
from django.views.generic import TemplateView

# URLs with with i18n
from pycones.schedules.views import pentabarf_view, xcal_view, icalendar_view

urlpatterns = i18n_patterns(
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^code-of-conduct/$', TemplateView.as_view(template_name='pages/code_of_conduct.html'), name="code-of-conduct"),
    url(r'^tickets/$', TemplateView.as_view(template_name='pages/tickets.html'), name="tickets"),
    url(r'^info/$', TemplateView.as_view(template_name='pages/info.html'), name="info"),
    url(r'^keynoters-speakers/$', TemplateView.as_view(template_name='pages/keynoters.html'), name="keynoters"),
    url(r'^blog/', include('pycones.blog.urls', namespace="blog")),
    url(r'^users/', include('pycones.users.urls', namespace="users")),
    url(r'^proposals/', include('pycones.proposals.urls', namespace="proposals")),
    url(r'^reviewers/', include('pycones.reviewers.urls', namespace="reviewers")),
    url(r'^schedule/', include('pycones.schedules.urls', namespace="schedule")),
    url(r'^jobboard/', include('pycones.jobboard.urls', namespace="jobboard")),
)

# URLs without i18n
urlpatterns += [
    url(r'schedule/pentabarf\.xml', pentabarf_view, name="schedule_pentabarf"),
    url(r'schedule/xcal\.xml', xcal_view, name="schedule_xcal"),
    url(r'schedule\.ics', icalendar_view, name="schedule_icalendar"),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

# Override all links if the landing page is set
if settings.LANDING_GLOBAL_REDIRECT:
    urlpatterns = [
        url(r'^$', TemplateView.as_view(template_name='pages/landing.html'), name="landing"),
    ]

# Django Admin, use {% url 'admin:index' %}
admin.site.site_header = _('%s Admin') % settings.CONFERENCE_TITLE
urlpatterns += [
    url(settings.ADMIN_URL, admin.site.urls),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]

    # If is installed debug_toolbar, add its urls
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

    # Only access directly to MEDIA when DEBUG is True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
