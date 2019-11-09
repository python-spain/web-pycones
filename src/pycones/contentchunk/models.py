from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from martor.models import MartorField


class Chunk(TimeStampedModel):
    """Content chunk"""

    name = models.CharField(max_length=20, verbose_name=_("name"))
    text = MartorField(
        _("Text"), blank=True, default="", help_text=_("Text in Markdown format")
    )
