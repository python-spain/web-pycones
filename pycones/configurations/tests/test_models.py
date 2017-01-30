# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import six
from django.test import TestCase

from pycones.configurations import INT, FLOAT, STRING
from pycones.configurations.models import Option
from pycones.configurations.tests.factories import OptionFactory


class OptionTests(TestCase):

    def test_get_existing_int_option(self):
        option = OptionFactory(name="option_int", public_name="option int", type=INT, value=10)
        value = Option.objects.get_value(name="option_int", default=0)
        self.assertIsInstance(value, int)
        self.assertEquals(value, option.get_value())

    def test_get_existing_float_option(self):
        option = OptionFactory(name="option_int", public_name="option int", type=FLOAT, value=10.1)
        value = Option.objects.get_value(name="option_int", default=0.5)
        self.assertIsInstance(value, float)
        self.assertEquals(value, option.get_value())

    def test_get_existing_string_option(self):
        option = OptionFactory(name="option_int", public_name="option int", type=STRING, value="foo")
        value = Option.objects.get_value(name="option_int", default="bar")
        self.assertIsInstance(value, six.text_type)
        self.assertEquals(value, option.get_value())
