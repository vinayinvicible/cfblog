__author__ = 'vinay'
import re
from django.conf.urls import url, include

from . import views
from .settings import CMS_BLOG_URL_PREFIX


blog_patterns = [
    url(r'^(?P<blog_category_slug>.+)/(?P<blog_post_slug>.+)',
        views.blog_post_index, name='cms_blog_posts_index'),
]

urlpatterns = [
    url(r'^{}/'.format(re.escape(CMS_BLOG_URL_PREFIX)),
        include(blog_patterns), name='cms_blog_posts_index'),

    url(r'^cms/ajax/save/(?P<save_type>.+)/$',
        views.save, name='save_cms_content'),

    url(r'^(?P<url_path>.+)/$',
        views.cms_page_index, name='cmspages_index'),
]
