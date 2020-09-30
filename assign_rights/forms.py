from django.forms import ModelForm, inlineformset_factory

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
