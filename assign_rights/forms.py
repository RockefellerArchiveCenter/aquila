from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django.forms import (ModelForm, Select, Textarea, TextInput,
                          inlineformset_factory)

from .models import Grouping, RightsGranted, RightsShell


class RightsShellCommonLayout(Layout):
    """Form layout for fields used across all RightsShellForms."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            Div(
                Div("determination_date", css_class="col"), css_class="row"),
            Div(
                Div("start_date", css_class="col-5"),
                Div("start_date_period", css_class="col-2"), css_class="row"),
            Div(
                Div("end_date", css_class="col-5"),
                Div("end_date_period", css_class="col-2"),
                Div("end_date_open", css_class="form-check rights-basis__checkbox"), css_class="row"),
            Div(
                Div("note", css_class="form-group col"),
                css_class="row")
        )


class GroupingForm(ModelForm):
    class Meta:
        model = Grouping
        fields = ["title", "description", "rights_shells"]


class RightsShellForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                Div('copyright_status', css_class="col-6"),
                Div('jurisdiction', css_class="col-6"), css_class="row"),
            RightsShellCommonLayout(),
        )

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            RightsShellCommonLayout(),
        )

    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'copyright_status',
            'jurisdiction',
            'license_terms',
            'statute_citation'
        )


class LicenseForm(RightsShellForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                Div('license_terms', css_class="col"), css_class="row"),
            RightsShellCommonLayout()
        )

    class Meta(RightsShellForm.Meta):
        exclude = (
            'rights_basis',
            'copyright_status',
            'jurisdiction',
            'statute_citation'
        )


class StatuteForm(RightsShellForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                Div('jurisdiction', css_class="col"), css_class="row"),
            Div(
                Div('statute_citation', css_class="col"), css_class="row"),
            RightsShellCommonLayout(),
        )

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
    can_delete=True
)
