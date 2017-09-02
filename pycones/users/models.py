# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from pycones.users.managers import UserManager
from pycones.utils.emails import send_template_email
from pycones.utils.generators import random_string


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    restore_code = models.CharField(max_length=16, null=True, blank=True, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def generate_restore_code(self):
        self.restore_code = random_string(16)
        self.save()

    def restore_password_link(self):
        return reverse("users:restore-password", kwargs={"restore_code": self.restore_code})

    def send_restore_password_link(self):
        """Sends email with link to restore password."""
        if not self.restore_code:
            self.generate_restore_code()
        context = {
            "user": self,
            "site": Site.objects.get_current()
        }
        send_template_email(
            subject=_("[%s] Establece tu contraseña") % settings.CONFERENCE_TITLE,
            from_email="%s <%s>" % (settings.CONFERENCE_TITLE, settings.CONTACT_EMAIL),
            to=self.email,
            template_name="emails/users/restore_email.html",
            context=context
        )

    def is_approved_speaker(self):
        """Check if the user is a speaker with an approved presentation."""
        try:
            return self.speaker.is_approved()
        except ObjectDoesNotExist:
            return False
