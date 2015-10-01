__author__ = 'vinay'
from django.contrib import admin

from .forms import CmsPageAdminForm
from .models import CmsPage, CmsBlogPost, CmsPageTemplate, CmsBlogCategory


class CmsTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(CmsPageTemplate, CmsTemplateAdmin)


class CmsPageCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(CmsBlogCategory, CmsPageCategoryAdmin)


class CmsPageAdmin(admin.ModelAdmin):
    pass
admin.site.register(CmsPage, CmsPageAdmin)


class CmsBlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status')
    list_filter = ('publish', 'category', 'sub_category', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}

    form = CmsPageAdminForm
admin.site.register(CmsBlogPost, CmsBlogPostAdmin)
