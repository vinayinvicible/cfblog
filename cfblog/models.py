from __future__ import unicode_literals

__author__ = 'vinay'

import datetime

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import resolve
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField
from tagging.fields import TagField

from .managers import CmsBlogCategoryManager, CmsBlogPostManager
from .utils import cacheable, stale_cache, get_public_data, get_image_path, get_file_path
from .validators import validate_and_get_template, validate_url_path


class CmsPageTemplate(models.Model):
    name = models.CharField(_('template name'), max_length=255, db_index=True, validators=[validate_and_get_template])

    def __unicode__(self):
        return self.name


STATUS_CHOICES = (
    (1, _('Draft')),
    (2, _('Public')),
)


class BaseCmsPage(models.Model):
    template = models.ForeignKey(CmsPageTemplate, verbose_name=_('template'), null=True, blank=True)
    auth_data = JSONField(verbose_name=_('author data'), default={}, blank=True)
    public_data = JSONField(verbose_name=_('public data'), default={}, blank=True)
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    modified_on = models.DateTimeField(_('modified on'), auto_now=True)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)

    class Meta:
        abstract = True

    @property
    def is_public(self):
        return self.status == 2

    def publish_cms_content(self):
        self.public_data = self.auth_data
        self.status = 2
        self.save()


class CmsPage(BaseCmsPage):
    url = models.CharField(_('url path'),
                           max_length=255, db_index=True, unique=True, validators=[validate_url_path])

    @cacheable('cms_page_{id}')
    def html(self):
        return get_public_data(self)

    @stale_cache('cms_page_{id}')
    def save(self, *args, **kwargs):
        super(CmsPage, self).save(*args, **kwargs)

    def clean(self):
        from .views import cms_page_index
        resolver_math = resolve(self.url)
        if resolver_math.func is cms_page_index and not self.template:
            raise ValidationError(_(
                'Template cannot be empty for new urls'
            ))

        if resolver_math.func is not cms_page_index and self.template:
            raise ValidationError(_(
                'Template is not required for existing urls'
            ))
        super(CmsPage, self).clean()


class CmsBlogCategory(models.Model):
    """Category model."""
    LEVEL_CHOICES = (
        (1, 1),
        (2, 2),
    )
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    slug = models.SlugField(_('slug'))
    parent = models.ForeignKey('self', blank=True, null=True)
    level = models.IntegerField(_('level'), choices=LEVEL_CHOICES)
    is_active = models.BooleanField(_('is_active'), default=True)
    objects = CmsBlogCategoryManager()

    class Meta:
        verbose_name_plural = _('cms blog page categories')
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class CmsBlogPost(BaseCmsPage):
    title = models.CharField(_('title'), max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    category = models.ForeignKey('CmsBlogCategory')
    tags = TagField()
    slug = models.SlugField(_('slug'), max_length=70)
    body = models.TextField(_('body'), null=True, blank=True)
    tease = models.TextField(_('tease'), blank=True,
                             help_text=_('Concise text suggested. Does not appear in RSS feed.'))
    keywords = models.TextField(_('keywords'), blank=True,
                                help_text=_('List of keywords, relevant for SEO'))
    # TODO: Include S3ImageField
    # thumbnail = ImageWithThumbsField(upload_to=get_image_path, sizes=(('s', 500, 500), ('r', 450, 600), ('t', 200, 260)), null=True, blank=True)
    infographic = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    pdf = models.FileField(upload_to=get_file_path, null=True, blank=True)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    sub_category = models.ForeignKey('CmsBlogCategory', related_name='sub_post_set', blank=True, null=True)
    related_posts = models.ManyToManyField('self', symmetrical=True, blank=True)
    notes_todos = models.TextField(_('Notes and Todos'), blank=True)
    votes = models.IntegerField(_('votes'), default=0)
    objects = CmsBlogPostManager()

    class Meta:
        ordering = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return self.title

    @cacheable('cms_blog_post_{id}')
    def html(self):
        return get_public_data(self)

    @stale_cache('cms_blog_post_{id}')
    def save(self, *args, **kwargs):
        super(CmsBlogPost, self).save(*args, **kwargs)

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)
