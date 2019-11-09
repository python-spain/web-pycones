# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _, get_language

from martor.models import MartorField
from model_utils.models import TimeStampedModel
from taggit_autosuggest.managers import TaggableManager

from pycones.blog import STATUSES, DRAFT
from pycones.blog.managers import ArticlesManager
from pycones.utils.files import UploadToDir


class AbstractArticle(TimeStampedModel):
    """Abstract model for articles, posts, etc."""

    status = models.PositiveIntegerField(choices=STATUSES, default=DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.TextField()
    slug = models.SlugField(blank=True, unique=True, max_length=128)
    content = MartorField(default="", blank=True)

    scheduled_at = models.DateTimeField(null=True, blank=True)

    outstanding_image = models.ImageField(
        upload_to=UploadToDir("images", random_name=False), null=True, blank=True
    )

    objects = ArticlesManager()

    class Meta:
        abstract = True


class Post(AbstractArticle):
    """Post for blogging"""

    tags = TaggableManager(
        verbose_name=_("Etiquetas"),
        help_text=_("Lista de etiquetas separadas por comas."),
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"slug": self.slug})

    def summary(self):
        """Split content using <!--more-->"""
        split_content = self.content.raw.split("<!--more-->")
        read_more = self._read_more_tag() if len(split_content) > 1 else ""
        return "{}{}".format(split_content[0], read_more)

    def save(self, **kwargs):
        slug_base = self.slug if self.slug else self.title
        self.slug = slugify(slug_base)
        super(Post, self).save(**kwargs)

