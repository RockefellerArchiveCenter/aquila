from rest_framework import serializers

from .models import RightsGranted, RightsShell


class RightsGrantedSerializer(serializers.ModelSerializer):
    """docstring"""
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    def get_start_date(self, object_start):
        return self.context.get("start_date")

    def get_end_date(self, object_end):
        return self.context.get("end_date")

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
    """Serializes instances of the RightsGranted model to fit within RAC rights schema"""
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    status = serializers.CharField(source="copyright_status")
    terms = serializers.CharField(source="license_terms")
    citation = serializers.CharField(source="statute_citation")
    rights_granted = serializers.ListField(default=[])

    def get_start_date(self, object_start):
        return self.context.get("start_date")

    def get_end_date(self, object_end):
        return self.context.get("end_date")

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
            "citation",
            "rights_granted"
        )
