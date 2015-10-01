__author__ = 'vinay'
from django import forms

from .models import CmsBlogPost
from .settings import CMS_BLOG_URL_PREFIX


class CmsPageAdminForm(forms.ModelForm):
    class Meta:
        model = CmsBlogPost
        fields = '__all__'

    def clean(self):
        super(CmsPageAdminForm, self).clean()
        form_data = self.cleaned_data
        # TODO: Need to include other blog dependent fields in validation
        if form_data.get('type', '') == 'blog_post':
            slug = form_data.get('slug')
            category = form_data.get('category')
            if not (slug and category):
                raise forms.ValidationError(
                    'Slug and Category cannot be empty for a blog post'
                )
            url = '/{}/{}/{}/'.format(CMS_BLOG_URL_PREFIX, category.slug, slug)
            form_data['url'] = url

        return form_data
