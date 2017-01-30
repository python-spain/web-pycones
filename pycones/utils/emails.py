# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from smtplib import SMTPAuthenticationError
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template, render_to_string


def send_template_email(subject, from_email, to, template_name, context=None):
    """
    :param subject:
    :param from_email:
    :param to: list or string
    :param template_name:
    :param context:
    """
    if context is None:
        context = {}
    current_site = Site.objects.get_current()
    context.update({
        "site": current_site,
        "static": "https://{}{}".format(
            current_site.domain,
            settings.STATIC_URL
        )
    })

    template = get_template(template_name)
    content = template.render(context)
    if not isinstance(to, list):
        to = [to]
    msg = EmailMultiAlternatives(subject, content, from_email, to)
    msg.attach_alternative(content, "text/html")
    try:
        msg.send()
    except SMTPAuthenticationError:
        pass


def send_email_multi_alternatives(subject, message_txt, message, from_email, to):
    """Sends an email using EmailMultiAlternatives"""
    email = EmailMultiAlternatives(subject=subject, body=message_txt, from_email=from_email, to=to)
    email.attach_alternative(message, "text/html")
    email.send()


def send_email(context, template, subject, from_email, to, content=None):
    """Sends an email using a template as content."""
    if not isinstance(to, list) and not isinstance(to, tuple):
        to = [to]
    if content is not None and 'content' not in context:
        context['content'] = content
    message = render_to_string(template, context)
    message_txt = message.replace("\n", "")
    message_txt = message_txt.replace("</p>", "\n")
    message_txt = message_txt.replace("</h1>", "\n\n")
    message_txt = bleach.clean(message_txt, strip=True)
    send_email_multi_alternatives(subject, message_txt, message, from_email, to)
