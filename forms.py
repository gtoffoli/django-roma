'''
Created on 25/feb/13
@author: Giovanni Toffoli
'''
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

class LivesearchForm(forms.Form):
    '''
    live search of all searchable contents based on full-text search
    '''
    searchtext = forms.CharField(
        label='Cerca',
        # widget=AutoCompleteWidget(EntryLookup),
        required=False,
        )

    def render_fields(self):
        # field_list = [str(field) for field in self]
        field_list = []
        for field in self:
            field_list.append(field.label)
            field_list.append(': ')
            field_list.append(str(field))
        return ' '.join(field_list)

class SearchForm(forms.Form):
    q = forms.CharField(label='Cerca nel sito',)

from allauth.account.forms import SignupForm as allauthSignupForm
# GT 131015
class SignupForm(allauthSignupForm):
    first_name = forms.CharField(
            label=_("First name"),
            required=True
            # widget=forms.TextInput(attrs={'class':'span6'})
            )
    last_name = forms.CharField(
            label=_("Last name"),
            required=True
            # widget=forms.TextInput(attrs={'class':'span6'})
            )

    def after_signup(self, user, **kwargs):
            user.first_name = self.cleaned_data["first_name"]
            user.last_name = self.cleaned_data["last_name"]
            user.save()
