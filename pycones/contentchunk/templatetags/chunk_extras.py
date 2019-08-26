from django import template
from pycones.contentchunk.models import Chunk

"""
Usage:

On your template add:

{% load chunk_extras %}

Then you can reference the chunk content as:

{% chunk name="test" as my_content %}

and use it whenever you want

<div>
{{my_content}}
</div>

"""

register = template.Library()


@register.simple_tag(takes_context=True)
def chunk(context, name):
    try:
        o = Chunk.objects.get(name=name)
    except Chunk.DoesNotExist:
        return ""
    return o.text

