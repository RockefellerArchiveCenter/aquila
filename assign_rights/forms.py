from django import forms
from django.forms import formset_factory

from .models import RightsGranted, RightsShell


class RightsShellModelForm(forms.ModelForm):
    """docstring for RightsShellForm"""
    class Meta:
        model = RightsShell
        fields = [
            'rights_basis',
            'copyright_status',
            'determination_date',
            'note',
            'applicable_start_date',
            'applicable_end_date',
            'start_date_period',
            'end_date_period',
            'end_date_open',
            'license_terms',
            'statute_citation'
        ]


class RightsGrantedModelForm(forms.ModelForm):
    """docstring for RightsShellForm"""
    class Meta:
        model = RightsGranted
        fields = [
            'basis',
            'act',
            'note',
            'start_date',
            'end_date',
            'start_date_period',
            'end_date_period',
            'end_date_open',
        ]


RightsGrantedFormSet = formset_factory(RightsGrantedModelForm)
