from rest_framework import serializers

from .models import RightsGranted, RightsShell


class RightsGrantedSerializer(serializers.ModelSerializer):
    """Serializes changes to the RightsGranted model to fit within RAC rights schema.
    The start date and end dates will be overwritten to include calculated dates.
    """
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    grant_restriction = serializers.CharField(source='restriction')

    class Meta:
        model = RightsGranted
        fields = (
            "act",
            "grant_restriction",
            "start_date",
            "end_date",
            "granted_note"
        )


class RightsShellSerializer(serializers.ModelSerializer):
    """Serializes changes to the RightsShell model to fit within RAC rights schema.
    The start date and end dates will be overwritten to include calculated dates.
    The rights granted field will be a list of any associated RightsGranted objects.
    """
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    rights_granted = serializers.ListField(default=[])
    jurisdiction = serializers.CharField()

    class Meta:
        model = RightsShell
        fields = (
            "rights_basis",
            "start_date",
            "end_date",
            "basis_note",
            "rights_granted"
        )


class RightsShellListSerializer(serializers.ModelSerializer):
    """Provides minimal information for API list view."""

    id = serializers.CharField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = RightsShell
        fields = ('id', 'title')

    def get_title(self, obj):
        return str(obj)


class OtherSerializer(RightsShellSerializer):
    rights_basis = serializers.SerializerMethodField()
    other_basis = serializers.CharField(source='rights_basis')

    class Meta:
        model = RightsShell
        fields = RightsShellSerializer.Meta.fields + ('other_basis',)

    def get_rights_basis(self, obj):
        return "other"


class CopyrightSerializer(RightsShellSerializer):

    class Meta:
        model = RightsShell
        fields = RightsShellSerializer.Meta.fields + ('determination_date', 'jurisdiction', 'copyright_status')


class StatuteSerializer(RightsShellSerializer):

    class Meta:
        model = RightsShell
        fields = RightsShellSerializer.Meta.fields + ('determination_date', 'jurisdiction', 'statute_citation')


class LicenseSerializer(RightsShellSerializer):

    class Meta:
        model = RightsShell
        fields = RightsShellSerializer.Meta.fields + ('terms',)
