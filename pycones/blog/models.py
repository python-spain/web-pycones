# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _, get_language

from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel
from taggit_autosuggest.managers import TaggableManager

from pycones.blog import STATUSES, DRAFT
from pycones.blog.managers import ArticlesManager
from pycones.utils.files import UploadToDir


class AbstractArticle(TimeStampedModel):
    """Abstract model for articles, posts, etc."""

    status = models.PositiveIntegerField(choices=STATUSES, default=DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.TextField()
    slug = models.SlugField(blank=True, unique=True, max_length=128)
    content = MarkupField(default="", default_markup_type="markdown", blank=True)

    scheduled_at = models.DateTimeField(null=True, blank=True)

    outstanding_image = models.ImageField(upload_to=UploadToDir('images', random_name=False), null=True, blank=True)

    objects = ArticlesManager()

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Post(AbstractArticle):
    """Post for blogging"""

    tags = TaggableManager(
        verbose_name=_("Etiquetas"),
        help_text=_("Lista de etiquetas separadas por comas."),
        blank=True
    )

    def __str__(self):
        return self.title

    def _read_more_tag(self):
        """
        <p><a href="{% url "post" slug=post.slug %}">{% trans "Seguir leyendo..." %}</a></p>
        @return:
        """
        return '<p><a href="{}">{}</a></p>'.format(
            reverse("blog:post", kwargs={'slug': self.slug}),
            _("Seguir leyendo...")
        )

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={"slug": self.slug})

    def summary(self):
        """Split content using <!--more-->"""
        split_content = self.content.raw.split("<!--more-->")
        read_more = self._read_more_tag() if len(split_content) > 1 else ""
        return "{}{}".format(
            split_content[0],
            read_more
        )

    def get_content(self):
        language = get_language()
        attr = "content_%s" % language
        if hasattr(self, attr) and getattr(self, attr).raw is not None and getattr(self, attr).raw != "":
            return getattr(self, attr)
        elif hasattr(self, attr) and (getattr(self, attr).raw is None or getattr(self, attr).raw == ""):
            return self.content_es
        return self.content

    def save(self, **kwargs):
        slug_base = self.slug if self.slug else self.title
        self.slug = slugify(slug_base)
        super(Post, self).save(**kwargs)

