import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from rest_framework.renderers import JSONRenderer

from .models import RightsShell
from .serializers import (CopyrightSerializer, LicenseSerializer,
                          OtherSerializer, RightsGrantedSerializer,
                          StatuteSerializer)


class RightsAssembler(object):
    """Assembles and returns a list of rights statements."""

    def run(self, rights_ids, request_start_date, request_end_date):
        """Assembles and returns rights statements given rights statement IDs and
        start and end dates.

        Args:
            rights_ids (list): a list of identifiers for rights statements.
            request_start_date (string): a string representation of the earliest date of a group of records
            request_end_date (string): a string representation of the latest date of a group of records
        """
        rights_shells = self.retrieve_rights(rights_ids)
        shell_data = []
        for shell in rights_shells:
            grant_data = []
            start_date, end_date = self.get_dates(shell, request_start_date, request_end_date)
            serialized_shell = self.create_json(shell, start_date, end_date)
            for grant in shell.rightsgranted_set.all():
                start_date, end_date = self.get_dates(grant, request_start_date, request_end_date)
                grant_data.append(self.create_json(grant, start_date, end_date))
            serialized_shell["rights_granted"] = grant_data
            shell_data.append(serialized_shell)
        return shell_data

    def retrieve_rights(self, rights_ids):
        """Retrieves rights statements matching identifiers."""
        return [RightsShell.objects.get(pk=ident) for ident in rights_ids]

    def get_dates(self, object, request_start_date, request_end_date):
        """Calculate rights start and end dates for a given object.

        Args:
            object (obj): a RightsShell or RightsGranted object.
            request_start_date (string): the start date for a group of records.
            request_end_date (string): the end date for a group of records.

        Returns:
            object_start, object_end (tuple): a tuple with two datetime objects
                representing the group of objects' start and end dates after
                calculation.
        """
        object_start = None
        object_end = None
        if getattr(object, "start_date"):
            object_start = getattr(object, "start_date")
        else:
            object_start = datetime.strptime(request_start_date, "%Y-%m-%d").date() + relativedelta(years=object.start_date_period)
        if getattr(object, "end_date_period"):
            object_end = datetime.strptime(request_end_date, "%Y-%m-%d").date() + relativedelta(years=object.end_date_period)
        elif getattr(object, "end_date"):
            object_end = getattr(object, "end_date")
        return object_start, object_end

    def create_json(self, obj, obj_start, obj_end):
        """Runs specific serializer against an object and creates a JSON-structured dict.

        Args:
            object (obj): a RightsShell or RightsGranted object.
            serializer_class (str): A serializer class (RightsShellSerializer or RightsGrantedSerializer)
            obj_start (datetime); a datetime object representing the group of object's start date
            obj_end (datetime); a datetime object representing the group of object's end date

        Returns:
            data (dict): a JSON structured dictionary based on the object passed.
        """
        obj.start_date = obj_start
        obj.end_date = obj_end
        if obj.__class__ == RightsShell:
            if obj.rights_basis == "copyright":
                serializer = CopyrightSerializer(obj)
            elif obj.rights_basis == "statute":
                serializer = StatuteSerializer(obj)
            elif obj.rights_basis == "license":
                serializer = LicenseSerializer(obj)
            else:
                serializer = OtherSerializer(obj)
        else:
            serializer = RightsGrantedSerializer(obj)
        bytes = JSONRenderer().render(serializer.data)
        return json.loads(bytes.decode("utf-8"))
