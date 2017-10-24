'''
Created on 25/feb/13
@author: Giovanni
'''
from __future__ import unicode_literals

from django import template
from roma.forms import LivesearchForm

register = template.Library()

@register.inclusion_tag('livesearch.html')
def livesearch():
    return {'form': LivesearchForm()}