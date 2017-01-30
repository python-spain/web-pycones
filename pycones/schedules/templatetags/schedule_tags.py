from __future__ import unicode_literals

from django import template

register = template.Library()


@register.simple_tag()
def slot_col_size(tracks):
    grid_columns = 12
    return "col-sm-{}".format(int(grid_columns/tracks))
