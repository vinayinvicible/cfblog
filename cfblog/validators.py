from __future__ import unicode_literals
__author__ = 'vinay'
import re

from django.template.loader import get_template, select_template, TemplateDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


def validate_and_get_template(name, using=None):
    if isinstance(name, (list, tuple)):
        return select_template(name, using=using)
    try:
        return get_template('{}.html'.format(name), using=using)
    except TemplateDoesNotExist:
        raise ValidationError(_('Unable to find {} in the configured template folders'.format(name)))


url_path_re = re.compile(r'^/(?:[-a-zA-Z0-9_]+/)*$')
validate_url_path = RegexValidator(
    url_path_re,
    _("Enter a valid 'url path'. Path should start and end with '/'."),
    'invalid'
)
