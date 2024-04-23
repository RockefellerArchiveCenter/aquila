from django.forms import (CheckboxInput, ChoiceField, HiddenInput, ModelForm, Select,
                          Textarea, TextInput, inlineformset_factory)
from django.forms.utils import ErrorList

from .models import Grouping, RightsGranted, RightsShell


class StrErrorList(ErrorList):
    def __str__(self):
        return self.as_str()

    def as_str(self):
        if not self:
            return ''
        return ', '.join([e for e in self])


class GroupingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Grouping
        fields = ["title", "description", 'rights_shells']
        labels = {
            'rights_shells': ''  # legend is used instead of label
        }

class RightsShellDates(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    rights_begin = ChoiceField(
        label="Start of Rights",
        choices=(("", "---------"),
                 ("start_date", "These rights start on a specific date"),
                 ("start_date_period", "These rights start after an embargo period"),
                 ("start_date_period_zero", "These rights start on creation date of materials")),
        widget=Select(attrs={'required': True, 'v-model': 'rightsBegin'}))
    rights_end = ChoiceField(
        label="End of Rights",
        choices=(("", "---------"),
                 ("end_date", "These rights end on a specific date"),
                 ("end_date_period", "These rights end after an embargo period"),
                 ("end_date_open", "There is no end date for these rights")),
        widget=Select(attrs={'required': True, 'v-model': 'rightsEnd'}))

    class Meta:
        model = RightsShell
        fields = [
            'rights_begin',
            'rights_end',
            'start_date',
            'end_date',
            'start_date_period',
            'end_date_period',
            'end_date_open',
        ]
        labels = {
            'start_date_period': "Start Date Embargo Period (in years)",
            'end_date_period': "End Date Embargo Period (in years)",
            'start_date': "Start Date (yyyy-mm-dd)",
            'end_date': "End Date (yyyy-mm-dd)",
        }
        widgets = {
            'start_date': TextInput(attrs={'required': True, 'pattern': "\\d{4}-\\d{2}-\\d{2}"}),
            'start_date_period': TextInput(attrs={'required': True}),
            'end_date': TextInput(attrs={'required': True, 'pattern': "\\d{4}-\\d{2}-\\d{2}"}),
            'end_date_period': TextInput(attrs={'required': True}),
            'end_date_open': HiddenInput(attrs={'value': True}),
        }

    def clean(self):
            cleaned_data = super().clean()
            end_date = cleaned_data.get("end_date")
            start_date = cleaned_data.get("start_date")

            if end_date and start_date:
                if start_date > end_date:
                    self.add_error('start_date', "The start date must be before the end date.")
                    self.add_error('end_date', "The end date must be after the start date.")

class RightsShellForm(ModelForm):
    dates = RightsShellDates()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    class Meta:
        model = RightsShell
        fields = [
            'rights_basis',
            'copyright_status',
            'jurisdiction',
            'determination_date',
            'basis_note',
            'start_date',
            'end_date',
            'start_date_period',
            'end_date_period',
            'end_date_open',
            'terms',
            'statute_citation'
        ]
        widgets = {
            'rights_basis': Select(attrs={'required': True, 'v-model': 'rightsBasisSelected'}),
        }

class RightsShellUpdateForm(RightsShellForm):
    dates = RightsShellDates()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    class Meta(RightsShellForm.Meta):
        widgets = {
            'rights_basis': Select(attrs={'disabled': 'disabled'}),
        }


class CopyrightForm(RightsShellForm):

    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'terms',
            'statute_citation'
        )
        widgets = {
            'copyright_status': Select(attrs={'required': True}),
            'jurisdiction': TextInput(attrs={'maxlength': '2', 'required': True}),
        }


class OtherForm(RightsShellForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'copyright_status',
            'determination_date',
            'jurisdiction',
            'terms',
            'statute_citation'
        )


class LicenseForm(RightsShellForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'copyright_status',
            'determination_date',
            'jurisdiction',
            'statute_citation'
        )


class StatuteForm(RightsShellForm):

    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'copyright_status',
            'terms'
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
            'granted_note',
            'start_date',
            'end_date',
            'start_date_period',
            'end_date_period',
            'end_date_open',
        ]

    def clean(self):
        cleaned_data = super().clean()
        end_date = cleaned_data.get("end_date")
        start_date = cleaned_data.get("start_date")

        if end_date and start_date:
            if start_date > end_date:
                self.add_error('start_date', "The start date must be before the end date.")
                self.add_error('end_date', "The end date must be after the start date.")


RightsGrantedFormSet = inlineformset_factory(
    RightsShell,
    RightsGranted,
    extra=0,
    form=RightsGrantedForm,
    can_delete=True
)
