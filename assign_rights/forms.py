from django.forms import (DateInput, ModelForm, NumberInput, Select, Textarea,
                          inlineformset_factory)

from .models import Grouping, RightsGranted, RightsShell


class GroupingForm(ModelForm):
    class Meta:
        model = Grouping
        fields = ["title", "description", "rights_shells"]


class RightsShellForm(ModelForm):
    class Meta:
        model = RightsShell
        fields = [
            'rights_basis',
            'copyright_status',
            'determination_date',
            'note',
            'start_date',
            'end_date',
            'start_date_period',
            'end_date_period',
            'end_date_open',
            'license_terms',
            'statute_citation'
        ]
        widgets = {
            'rights_basis': Select(attrs={'v-model': 'selected', 'class': 'form-control'}),
            'copyright_status': Select(attrs={'class': 'form-control'}),
            'determination_date': DateInput(attrs={'class': 'form-control'}),
            'note': Textarea(attrs={'class': 'form-control'}),
            'start_date': DateInput(attrs={'class': 'form-control'}),
            'end_date': DateInput(attrs={'class': 'form-control'}),
            'start_date_period': NumberInput(attrs={'class': 'form-control'}),
            'end_date_period': NumberInput(attrs={'class': 'form-control'}),
            'license_terms': Textarea(attrs={'class': 'form-control'}),
            'statute_citation': Textarea(attrs={'class': 'form-control'})
        }


class RightsGrantedForm(ModelForm):
    class Meta:
        model = RightsGranted
        fields = [
            'basis',
            'restriction',
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
