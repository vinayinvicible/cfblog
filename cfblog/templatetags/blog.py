import re
import collections

from django import template
from django.conf import settings
from django.db import models
from django.template.defaultfilters import stringfilter


Post = models.get_model('blog', 'post')
Category = models.get_model('blog', 'category')

register = template.Library()


class LatestPosts(template.Node):

    def __init__(self, limit, var_name):
        self.limit = int(limit)
        self.var_name = var_name

    def render(self, context):
        posts = Post.objects.published()[:self.limit]
        if posts and (self.limit == 1):
            context[self.var_name] = posts[0]
        else:
            context[self.var_name] = posts
        return ''


@register.tag
def get_latest_posts(parser, token):
    """
    Gets any number of latest posts and stores them in a varable.

    Syntax::

        {% get_latest_posts [limit] as [var_name] %}

    Example usage::

        {% get_latest_posts 10 as latest_post_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[
            0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return LatestPosts(format_string, var_name)


class BlogCategories(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        categories = Category.objects.all()
        context[self.var_name] = categories
        return ''


@register.tag
def get_blog_categories(parser, token):
    """
    Gets all blog categories.

    Syntax::

        {% get_blog_categories as [var_name] %}

    Example usage::

        {% get_blog_categories as category_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[
            0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return BlogCategories(var_name)


@register.filter
def get_links(value):
    """
    Extracts links from a ``Post`` body and returns a list.

    Template Syntax::

        {{ post.body|markdown:"safe"|get_links }}

    """
    try:
        try:
            from BeautifulSoup import BeautifulSoup
        except ImportError:
            from beautifulsoup import BeautifulSoup
        soup = BeautifulSoup(value)
        return soup.findAll('a')
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in 'get_links' filter: BeautifulSoup isn't installed."
    return value


@register.filter
def get_tag_search_url(value):
    """
    Takes a tag (jargon term) and return its relevant
     jargon search url

    Template Syntax::

        {{ tag|get_tag_search_url }}

    """
    tag_link = "/articles/jargon_search/?jq=%s" % (
        value.lower().strip().replace(' ', '+'))
    return tag_link


@register.filter
@stringfilter
def commator(value, price=""):
    """ adds commas to a number in indian 1234556.234|commator -> Rs. 12,34,556.234
    123456|commator:auto -> Rs. 1.23 lac.
    """
    li = value.split(".")
    value = li[0]
    try:
        rest = li[1]
    except IndexError:
        rest = "00"

    strval = value[::-1]

    if strval:
        strnew = strval[0]
        strval = strval[1:]

    for i in range(len(strval)):
        if i % 2 == 1:
            strnew += strval[i] + ","
        else:
            strnew += strval[i]
    strret = strnew[::-1]
    if rest:
        strret += ".%s" % rest

    pricedi = collections.OrderedDict([("none", ""), ("thousand", "K."), ("lakh", "lac."), ("crore", "cr."), (
        "arab", "ar."), ("kharab", "khr."), ("neel", "nl."), ("padma", "pd."), ("shankh", "shk.")])

    suffix = ""
    if price == "auto":
        li = strret.split(",")
        suffix = pricedi.values()[len(li) - 1]
        strret = li[0]
        if len(li) > 1:
            strret += "." + li[1][:2]
    elif price in pricedi.keys():
        # TODO: Yet to implement
        li = strret.split(",")
        iter = -1
        for k, v in pricedi:
            iter += 1
            if k == price:
                val = v
                break
        if iter > 0:
            strret = "".join(li[:0 - iter]) + "." + li[0 - iter][:2]
    else:
        pass
    if strret and strret[0] == ',' and len(strret) > 1:
        strret = strret[1:]
    strret = u"\u20B9. " + strret + " %s" % suffix
    return strret
