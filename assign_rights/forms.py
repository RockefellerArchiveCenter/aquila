from django import forms

from .models import RightsShell


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
