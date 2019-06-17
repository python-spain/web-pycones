from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from markupfield.fields import MarkupField


class Chunk(TimeStampedModel):
    """Content chunk"""

    name = models.CharField(max_length=20, verbose_name=_("name"))
    text = MarkupField(
        _("Text"),
        blank=True,
        default="",
        default_markup_type="markdown",
        help_text=_("Text in Markdown format"),
    )
