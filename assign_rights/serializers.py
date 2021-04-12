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
    status = serializers.CharField(source="copyright_status")
    terms = serializers.CharField(source="license_terms")
    rights_granted = serializers.ListField(default=[])
    jurisdiction = serializers.SerializerMethodField()

    class Meta:
        model = RightsShell
        fields = (
            "rights_basis",
            "determination_date",
            "jurisdiction",
            "start_date",
            "end_date",
            "note",
            "status",
            "terms",
            "statute_citation",
            "rights_granted"
        )

    def get_jurisdiction(self, obj):
        return obj.jurisdiction.lower() if obj.jurisdiction else None
