#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _
from django.views import defaults as default_views
from django.views.generic import TemplateView

from pycones.schedules.views import pentabarf_view, xcal_view, icalendar_view


# URLs with with i18n


class PyconESAdminSite(AdminSite):
    site_header = "Python 2019 Admin"


admin_site = PyconESAdminSite(name="PyconES 2019")

urlpatterns = i18n_patterns(
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "hotels/",
        TemplateView.as_view(template_name="pages/hotels.html"),
        name="hotels",
    ),
    path(
        "call-for-papers/",
        TemplateView.as_view(template_name="pages/call_for_papers.html"),
        name="cfp",
    ),
    path(
        "horario/",
        TemplateView.as_view(template_name="pages/schedule.html"),
        name="horario",
    ),
    path(
        "code-of-conduct/",
        TemplateView.as_view(template_name="pages/code_of_conduct.html"),
        name="code-of-conduct",
    ),
    path("info/", TemplateView.as_view(template_name="pages/info.html"), name="info"),
    path("blog/", include("pycones.blog.urls", namespace="blog")),
    path("users/", include("pycones.users.urls", namespace="users")),
    path("proposals/", include("pycones.proposals.urls", namespace="proposals")),
    path("reviewers/", include("pycones.reviewers.urls", namespace="reviewers")),
    path("schedule/", include("pycones.schedules.urls", namespace="schedule")),
    path("jobboard/", include("pycones.jobboard.urls", namespace="jobboard")),
    path("tshirts/", include("pycones.tshirts.urls", namespace="tshirts")),
    # markdown editor
    path("martor/", include("martor.urls")),
    prefix_default_language=False,
)

# URLs without i18n
urlpatterns += [
    path("taggit_autosuggest/", include("taggit_autosuggest.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
]

# Override all links if the landing page is set
if settings.LANDING_GLOBAL_REDIRECT:
    urlpatterns = [
        path(
            "", TemplateView.as_view(template_name="pages/landing.html"), name="landing"
        )
    ]

# Django Admin, use {% url 'admin:index' %}
admin.site.site_header = _("%s Admin") % settings.CONFERENCE_TITLE
urlpatterns += [url(settings.ADMIN_URL, admin.site.urls)]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

    # If is installed debug_toolbar, add its urls
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            # For django versions before 2.0:
            # url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    # Only access directly to MEDIA when DEBUG is True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
