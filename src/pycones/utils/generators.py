# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from PIL import Image


def random_upper(a_string):
    """
    :param a_string
    """
    def aleatory_upper(char):
        flag = random.choice([True, False])
        if flag:
            return char.upper()
        return char

    return ''.join([aleatory_upper(character) for character in a_string])


def random_hexadecimal(length=16):
    """ Generates a random hexadecimal string.

    :param length: Lengtht of the generated string.
    """
    hexdigits = string.hexdigits
    return ''.join(random.choice(hexdigits) for _ in range(length))


def unique_random_hexadecimal(django_cls, length=16):
    """ Generates a random hexadecimal string, unique in code field from a django class model

    :param length: Length of the generated string.
    :param django_cls: Django class, it has a code field.
    """
    code = random_hexadecimal(length)
    while django_cls.objects.filter(close2me_id=code).exists():
        length += random.choice([-1, 1])
        code = random_hexadecimal(length)
    return random_upper(code)


def random_string(length=16):
    """ Generates a random alphanumeric string.

    :param length: Lengtht of the generated string.
    """
    chars = string.digits + string.ascii_letters
    return u''.join(random.choice(chars) for _ in range(length))


def random_pin(length=4):
    """ Generates a randon numeric string

    :param length: Lengtht of the generated string.
    """
    chars = string.digits
    return u''.join(random.choice(chars) for _ in range(length))


def random_image(size=(200, 200)):
    """ Generates a random PIL image, for testings propouse.

    :param size: Size of the random image generated.
    """
    color = (random.randint(0, 255), random.randint(0, 255),
             random.randint(0, 255), 0)
    return Image.new("RGBA", size, color)
