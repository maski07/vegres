from django import forms

class SearchYelpResForm(forms.Form):
    term = forms.CharField(label='term')
    location = forms.CharField(label='term')
