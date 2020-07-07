from django import forms

from .models import Grouping, RightsShell


class GroupingForm(forms.ModelForm):
    """docstring for RightsShellForm"""
    class Meta:
        model = Grouping
        fields = ["title", "description", "rights_shells"]
