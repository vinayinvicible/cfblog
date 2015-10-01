# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import re
import cfblog.validators
import tagging.fields
import jsonfield.fields
import cfblog.utils
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CmsBlogCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('slug', models.SlugField(verbose_name='slug')),
                ('level', models.IntegerField(verbose_name='level', choices=[(1, 1), (2, 2)])),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('parent', models.ForeignKey(blank=True, to='cfblog.CmsBlogCategory', null=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name_plural': 'cms blog page categories',
            },
        ),
        migrations.CreateModel(
            name='CmsBlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_data', jsonfield.fields.JSONField(default={}, verbose_name='author data', blank=True)),
                ('public_data', models.TextField(default='', verbose_name='public data', blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='modified on')),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(1, 'Draft'), (2, 'Public')])),
                ('publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='publish')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('slug', models.SlugField(max_length=70, verbose_name='slug')),
                ('body', models.TextField(null=True, verbose_name='body', blank=True)),
                ('tease', models.TextField(help_text='Concise text suggested. Does not appear in RSS feed.', verbose_name='tease', blank=True)),
                ('keywords', models.TextField(help_text='List of keywords, relevant for SEO', verbose_name='keywords', blank=True)),
                ('infographic', models.ImageField(null=True, upload_to=cfblog.utils.get_image_path, blank=True)),
                ('pdf', models.FileField(null=True, upload_to=cfblog.utils.get_file_path, blank=True)),
                ('allow_comments', models.BooleanField(default=True, verbose_name='allow comments')),
                ('notes_todos', models.TextField(verbose_name='Notes and Todos', blank=True)),
                ('votes', models.IntegerField(default=0, verbose_name='votes')),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('category', models.ForeignKey(to='cfblog.CmsBlogCategory')),
                ('related_posts', models.ManyToManyField(related_name='related_posts_rel_+', to='cfblog.CmsBlogPost', blank=True)),
                ('sub_category', models.ForeignKey(related_name='sub_post_set', blank=True, to='cfblog.CmsBlogCategory', null=True)),
            ],
            options={
                'ordering': ('-publish',),
                'get_latest_by': 'publish',
            },
        ),
        migrations.CreateModel(
            name='CmsPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_data', jsonfield.fields.JSONField(default={}, verbose_name='author data', blank=True)),
                ('public_data', models.TextField(default='', verbose_name='public data', blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='modified on')),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(1, 'Draft'), (2, 'Public')])),
                ('publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='publish')),
                ('url', models.CharField(db_index=True, unique=True, max_length=255, verbose_name='url path', validators=[django.core.validators.RegexValidator(re.compile('^/(?:[-a-zA-Z0-9_]+/)*$'), "Enter a valid 'url path'. Path should start and end with '/'.", 'invalid')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CmsPageTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='template name', validators=[cfblog.validators.validate_and_get_template])),
            ],
        ),
        migrations.AddField(
            model_name='cmspage',
            name='template',
            field=models.ForeignKey(verbose_name='template', to='cfblog.CmsPageTemplate'),
        ),
        migrations.AddField(
            model_name='cmsblogpost',
            name='template',
            field=models.ForeignKey(verbose_name='template', to='cfblog.CmsPageTemplate'),
        ),
    ]
