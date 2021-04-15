from rest_framework import serializers

from .models import RightsGranted, RightsShell


class RightsGrantedSerializer(serializers.ModelSerializer):
    """Serializes changes to the RightsGranted model to fit within RAC rights schema.
    The start date and end dates will be overwritten to include calculated dates.
    """
    start_date = serializers.CharField()
    end_date = serializers.CharField()

    class Meta:
        model = RightsGranted
        fields = (
            "act",
            "restriction",
            "start_date",
            "end_date",
            "note"
        )


class RightsShellSerializer(serializers.ModelSerializer):
    """Serializes changes to the RightsShell model to fit within RAC rights schema.
    The start date and end dates will be overwritten to include calculated dates.
    The rights granted field will be a list of any associated RightsGranted objects.
    """
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    rights_granted = serializers.ListField(default=[])

    class Meta:
        model = RightsShell
        fields = (
            "rights_basis",
            "start_date",
            "end_date",
            "note",
            "rights_granted"
        )


class OtherSerializer(RightsShellSerializer):
    rights_basis = serializers.SerializerMethodField()
    other_basis = serializers.SerializerMethodField()

    class Meta:
        model = RightsShell
        fields = RightsShellSerializer.Meta.fields + ('other_basis',)

    def get_rights_basis(self, obj):
        return "other"

    def get_other_basis(self, obj):
        return obj.rights_basis


class CopyrightSerializer(RightsShellSerializer):
    jurisdiction = serializers.SerializerMethodField()

    class Meta:
        model = RightsShell
        fields = RightsShellSerializer.Meta.fields + ('determination_date', 'jurisdiction', 'copyright_status')

    def get_jurisdiction(self, obj):
        return obj.jurisdiction.lower() if obj.jurisdiction else None


class StatuteSerializer(RightsShellSerializer):
    jurisdiction = serializers.SerializerMethodField()

    class Meta:
        model = RightsShell
        fields = RightsShellSerializer.Meta.fields + ('determination_date', 'jurisdiction', 'statute_citation')

    def get_jurisdiction(self, obj):
        return obj.jurisdiction.lower() if obj.jurisdiction else None


class LicenseSerializer(RightsShellSerializer):

    class Meta:
        model = RightsShell
        fields = RightsShellSerializer.Meta.fields + ('license_terms',)
