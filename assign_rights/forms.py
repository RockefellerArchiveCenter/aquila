from django.forms import ModelForm, inlineformset_factory

from .models import RightsGranted, RightsShell


class RightsShellForm(ModelForm):
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


class RightsGrantedForm(ModelForm):
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


RightsGrantedFormSet = inlineformset_factory(
    RightsShell,
    RightsGranted,
    extra=1,
    form=RightsGrantedForm,
)
