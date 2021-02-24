from django.forms import (ModelForm, Select, Textarea, TextInput,
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
            'jurisdiction',
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
            'rights_basis': Select(attrs={'v-model': 'selected', }),
        }


class RightsShellUpdateForm(RightsShellForm):
    class Meta(RightsShellForm.Meta):
        widgets = {
            'rights_basis': Select(attrs={'disabled': 'disabled'})
        }


class CopyrightForm(RightsShellForm):
    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'license_terms',
            'statute_citation'
        )
        widgets = {
            'copyright_status': Select(attrs={'required': True}),
            'jurisdiction': TextInput(attrs={'maxlength': '2', 'required': True}),
        }


class OtherForm(RightsShellForm):
    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'copyright_status',
            'jurisdiction',
            'license_terms',
            'statute_citation'
        )


class LicenseForm(RightsShellForm):
    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'copyright_status',
            'jurisdiction',
            'statute_citation'
        )


class StatuteForm(RightsShellForm):
    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'copyright_status',
            'license_terms',
        )
        widgets = {
            'jurisdiction': TextInput(attrs={'maxlength': '2', 'required': True}),
            'statute_citation': Textarea(attrs={'required': True})
        }


class RightsGrantedForm(ModelForm):
    class Meta:
        model = RightsGranted
        fields = [
            'basis',
            'act',
            'restriction',
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
    extra=0,
    form=RightsGrantedForm,
    can_delete=False
)
