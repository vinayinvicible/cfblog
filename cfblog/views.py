__author__ = 'vinay'
import json
import traceback

from django.http.response import HttpResponseForbidden, HttpResponseBadRequest
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.utils.module_loading import import_string

from .models import CmsPage, CmsBlogPost
from .response import cms_response
from .settings import CMS_AUTH_TEST_FUNC
from .utils import publish_cms_content, dum_request, NAMESPACE_DELIMITER, user_passes_test


def cms_page_index(request, url_path='', cms_page=None):
    if not (url_path or cms_page):
        raise ValueError(
            'Either url_path or cms_page should be passed'
        )

    if not cms_page:
        url_path = u'/{}/'.format(url_path.strip('/'))
        cms_page = get_object_or_404(CmsPage, url=url_path)

    if CMS_AUTH_TEST_FUNC(request.user):
        return cms_response(
            template_name=cms_page.template.name,
            cms_context=cms_page.auth_data,
            request=request,
            template_context={'view': 'author',
                              'cms_data': json.dumps(cms_page.auth_data),
                              'cms_page_class': '{}.{}'.format(cms_page.__module__, cms_page.__class__.__name__),
                              'id': cms_page.id,
                              'namespace_delimiter': json.dumps(NAMESPACE_DELIMITER)})

    if cms_page.is_public:
        return HttpResponse(cms_page.html)

    raise Http404("page not found")


def blog_post_index(request, blog_category_slug, blog_post_slug):
    blog_post = get_object_or_404(CmsBlogPost, slug=blog_post_slug, category__slug=blog_category_slug)
    return cms_page_index(request, cms_page=blog_post)


@require_POST
@csrf_protect
@user_passes_test()
def save(request, save_type):
    if not request.is_ajax():
        return HttpResponseForbidden()

    post_data = request.POST
    if any(_ not in post_data for _ in ('auth_data', 'cms_page_class', 'cms_page_id')) \
            or save_type not in ('draft', 'publish'):
        return HttpResponseBadRequest(content=json.dumps({'success': False}),
                                      content_type='application/json')

    try:
        CmsPage = import_string(post_data['cms_page_class'])
    except ImportError:
        return HttpResponseBadRequest(content=json.dumps({'success': False}),
                                      content_type='application/json')
    else:
        cms_page = get_object_or_404(CmsPage, id=post_data['cms_page_id'])

    try:
        content = json.loads(post_data['auth_data'])
    except:
        return HttpResponseBadRequest(content=json.dumps({'success': False,
                                                          'message': 'Invalid JSON object'}),
                                      content_type='application/json')
    else:
        cms_page.auth_data.update(content)
        try:
            cms_response(cms_page.template.name, cms_context=cms_page.auth_data)
        except Exception as e:
            return HttpResponse(content=json.dumps({'success': False,
                                                    'message': 'Unable to parse the new content.\n'
                                                               'Please resolve the issues and try again',
                                                    'exception': e,
                                                    'traceback': traceback.format_exc()}),
                                content_type='application/json')
        cms_page.save()
        if save_type == 'draft':
            return HttpResponse(content=json.dumps({'success': True}),
                                content_type='application/json')
        else:
            return publish_cms_content(cms_page,
                                       request=dum_request)
