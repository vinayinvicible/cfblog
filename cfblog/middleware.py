__author__ = 'vinay'
from django.conf import settings
from django.http.response import HttpResponse

from .models import CmsPage
from .settings import CMS_AUTH_TEST_FUNC
from .utils import parse_cms_template
from .views import cms_page_index


class CmsPageMiddleware(object):

    def process_response(self, request, response):
        # ignore all ajax, static and media requests
        if request.is_ajax() or \
                request.path.startswith(settings.STATIC_URL or '///') or \
                request.path.startswith(settings.MEDIA_URL or '///'):
            return response

        try:
            # TODO: Discuss with amitu. Caching with template context won't work in all cases
            cms_page = CmsPage.objects.get(url=request.path)
        except:
            pass
        else:
            # process only successful and 404 responses
            if response.status_code == 404:
                return cms_page_index(request, url_path=request.path, cms_page=cms_page)
            elif 200 <= response.status_code < 300:
                if CMS_AUTH_TEST_FUNC(request.user):
                    content = parse_cms_template(response.content, cms_page.auth_data)
                    return HttpResponse(content)
                elif cms_page.is_live:
                    return HttpResponse(cms_page.html)

        return response
