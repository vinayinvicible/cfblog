__author__ = 'vinay'
from .settings import CFCMS_TEMPLATE_DIRS


class CmsException(Exception):
    """ Base exception for all the cfcms exceptions. """
    pass


class CmsInvalidTemplateException(CmsException):
    def __init__(self, template_name):
        super(CmsInvalidTemplateException, self).__init__()
        self.message = u"Unable to find the template {}.\n" \
                       u"Tried in the following paths\n" \
                       u"{}".format(template_name,
                                    u'\n'.join(CFCMS_TEMPLATE_DIRS))


class CmsInvalidContent(CmsException):
    message = 'Invalid content'
