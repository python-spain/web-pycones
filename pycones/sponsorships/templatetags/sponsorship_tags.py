# -*- coding: utf-8 -*-
from django import template
from pycones.sponsorships.models import Sponsor, SponsorLevel

register = template.Library()


class SponsorsNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3 and bits[1] == "as":
            return cls(bits[2])
        elif len(bits) == 4 and bits[2] == "as":
            return cls(bits[3], bits[1])
        else:
            raise template.TemplateSyntaxError(
                "%r takes 'as var' or 'level as var'" % bits[0]
            )

    def __init__(self, context_var, level=None):
        if level:
            self.level = template.Variable(level)
        else:
            self.level = None
        self.context_var = context_var

    def render(self, context):
        if self.level:
            level = self.level.resolve(context)
            queryset = Sponsor.objects.filter(level__pk=level, active=True).order_by(
                "-sponsor_order", "created"
            )
        else:
            queryset = Sponsor.objects.filter(active=True).order_by(
                "level__order", "-sponsor_order", "created"
            )
        context[self.context_var] = queryset
        return ""


class SponsorLevelNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3 and bits[1] == "as":
            return cls(bits[2])
        else:
            raise template.TemplateSyntaxError("%r takes 'as var'" % bits[0])

    def __init__(self, context_var):
        self.context_var = context_var

    def render(self, context):
        context[self.context_var] = SponsorLevel.objects.all()
        return ""


@register.tag
def sponsors(parser, token):
    """
    {% sponsors as all_sponsors %}
    or
    {% sponsors "gold" as gold_sponsors %}
    """
    return SponsorsNode.handle_token(parser, token)


@register.tag
def sponsor_levels(parser, token):
    """
    {% sponsor_levels as levels %}
    """
    return SponsorLevelNode.handle_token(parser, token)
