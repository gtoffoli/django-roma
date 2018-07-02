'''
Created on 25/feb/13
@author: Giovanni Toffoli
'''
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField, CaptchaTextInput

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

#180417 MMR
class ContactForm(forms.Form):
    from_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':_("Full Name"),}))
    from_email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':_("Email"),}))
    subject = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':_("Subject")}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control','placeholder':_("Message")}))
    permission = forms.BooleanField(required=True, label=_('Pursuant to art. 13 of Legislative Decree 30 June 2003 n. 196 we wish to inform you that the personal data supplied by you with the completion and submission of this form will be used only to respond to your request.'), widget=forms.CheckboxInput())
    captcha = CaptchaField(
            label=_("control string"),
            help_text=_("Enter these 5 characters in the textbox on the right"),
            widget=CaptchaTextInput(attrs={'class': 'form-control'})
            )

#180702 MMR
class FlatPageForm(forms.Form):
    title = forms.CharField(required=True, label=_('title'), widget=forms.TextInput(attrs={'class':'form-control',}))
    content = forms.CharField(required=False, label=_('page content'), widget=forms.Textarea(attrs={'class':'form-control richtext', 'rows': 8, 'cols': 80,}))
