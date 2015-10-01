__author__ = 'vinay'
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


def _get_setting(setting, default_value):
    setting_value = getattr(settings, setting, default_value)

    if setting_value is default_value:
        return setting_value

    if not isinstance(setting_value, type(default_value)) and isinstance(setting_value, (unicode, str)):
        return import_string(setting_value)

    raise ImproperlyConfigured(
        '{} should be of type {} or should be a dotted module path, '
        'instead got {}'.format(setting, type(setting_value), type(default_value))
    )

CMS_AUTH_TEST_FUNC = _get_setting('AUTH_TEST_FUNC', lambda user: user.is_staff or user.is_superuser)
CMS_BLOG_URL_PREFIX = u'{}'.format(_get_setting('CMS_BLOG_URL_PREFIX', 'articles/').strip('/'))
CMS_TEMPLATE_DIRS = _get_setting('CMS_TEMPLATE_DIRS', settings.TEMPLATE_DIRS)

PAGE_CACHE_TIMEOUT = _get_setting('PAGE_CACHE_TIMEOUT', 60 * 60)
