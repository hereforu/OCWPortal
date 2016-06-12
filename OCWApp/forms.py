# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select your json file',
        help_text='max. 42 megabytes'
    )

class SearchForm(forms.Form):
	search_keyword = forms.CharField(
		label='searchpage',
		max_length=100)