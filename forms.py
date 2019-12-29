from django import forms

from .models import DictionaryQuery

class DictionaryQueryModelForms(forms.ModelForm):

    class Meta:
        model = DictionaryQuery
        fields = ['word']
