__author__ = 'vinay'
from django.core.exceptions import ValidationError
from django.http.response import Http404, HttpResponse
from django.template import TemplateSyntaxError

from .models import CmsPage
from .settings import CMS_TEMPLATE_DIRS, CMS_AUTH_TEST_FUNC
from .utils import parse_cms_template
from .validators import validate_and_get_template


def cms_response(template_name,
                 template_context=None, content_type=None, status=None,
                 using=None, request=None, cms_context=None):
    """
    Validates the given template and parses it's content
    returning HttpResponse or raising Http404 for syntax and template errors
    that are included in the cms_context

    This function is a hybrid of django's render and render_to_response by removing the deprecated arguments
    This also takes an optional parameter `cms_context` which is used to render the template.
    """
    try:
        cms_template = validate_and_get_template(template_name, using=using)
    except ValidationError:
        raise Http404(
            u"Unable to find the template {}.\n"
            u"Tried in the following paths\n"
            u"{}".format(template_name,
                         '\n'.join(CMS_TEMPLATE_DIRS)))
    else:
        content = cms_template.render(context=template_context,
                                      request=request)

        try:
            cms_page = CmsPage.objects.get(url=request.path)
        except CmsPage.DoesNotExist:
            pass
        else:
            if CMS_AUTH_TEST_FUNC(request.user):
                cms_context = cms_page.auth_data
            elif cms_page.is_live:
                return HttpResponse(cms_page.html, content_type, status)

        if cms_context is not None:
            if isinstance(cms_context, dict):
                # try:
                content = parse_cms_template(content, cms_context,
                                             publish=False)
                # except (ValidationError, TemplateSyntaxError):
                #     raise Http404()
            else:
                raise ValueError('cms_context should be a dict')

        return HttpResponse(content, content_type, status)
