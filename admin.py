from __future__ import unicode_literals

# from django.contrib import admin
from django.contrib.gis import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage
## OOPS this is a custom widget that works for initializing
## tinymce instances on stacked and tabular inlines
## for flatpages, just use the tinymce packaged one.
#from content.widgets import TinyMCE 
from tinymce.widgets import TinyMCE

class PageForm(FlatpageForm):

    class Meta:
        model = FlatPage
        widgets = {
            'content' : TinyMCE(),
        }
        fields = '__all__'

class PageAdmin(FlatPageAdmin):
    """
    Page Admin
    """
    form = PageForm
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)

