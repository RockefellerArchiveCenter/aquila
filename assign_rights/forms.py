from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Hidden, Layout
from django.forms import (ChoiceField, ModelForm, Select, Textarea, TextInput,
                          inlineformset_factory)

from .models import Grouping, RightsGranted, RightsShell


class RightsShellCommonLayout(Layout):
    """Form layout for fields used across all RightsShellForms."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            Div(
                Div("determination_date", css_class="col"), css_class="row"),
            Div(
                Div(Field("rights_begin", v_model="rightsBegin"), css_class="col-5"),
                Div("start_date", css_class="col-3", v_if="rightsBegin=='start_date'"),
                Div("start_date_period", css_class="col-3", v_if="rightsBegin=='start_date_period'"), css_class="row"),
            Div(
                Div(Field("rights_end", v_model="rightsEnd"), css_class="col-5"),
                Div("end_date", css_class="col-3", v_if="rightsEnd=='end_date'"),
                Div("end_date_period", css_class="col-3", v_if="rightsEnd=='end_date_period'"),
                Div(Hidden(name="end_date_open", value="true",), v_if="rightsEnd=='end_date_open'"), css_class="row"),
            Div(
                Div("note", css_class="form-group col"),
                css_class="row")
        )


class GroupingForm(ModelForm):
    class Meta:
        model = Grouping
        fields = ["title", "description", "rights_shells"]


class RightsShellForm(ModelForm):
    rights_begin = ChoiceField(
        label="Start of Rights",
        choices=(("", "---------"),
                 ("start_date", "These rights start on a specific date"),
                 ("start_date_period", "These rights start after an embargo period")))
    rights_end = ChoiceField(
        label="End of Rights",
        choices=(("", "---------"),
                 ("end_date", "These rights end on a specific date"),
                 ("end_date_period", "These rights end after an embargo period"),
                 ("end_date_open", "There is no end date for these rights")))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_template = "forms/custom_field.html"
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
        labels = {
            'start_date_period': "Start Date Embargo Period",
            'end_date_period': "End Date Embargo Period",
        }
        widgets = {
            'rights_basis': Select(attrs={'v-model': 'rightsBasisSelected', }),
        }


class RightsShellUpdateForm(RightsShellForm):
    class Meta(RightsShellForm.Meta):
        widgets = {
            'rights_basis': Select(attrs={'disabled': 'disabled'}),
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
