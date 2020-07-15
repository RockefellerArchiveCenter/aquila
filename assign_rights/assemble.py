import json

from datetime import datetime

from dateutil.relativedelta import relativedelta
from rest_framework.renderers import JSONRenderer

from .models import RightsShell
from .serializers import RightsGrantedSerializer, RightsShellSerializer

# Receive POST request that contains multiple rights IDs and one date
# For each rights ID, take date to calculate and return rights json (that looks like what Aurora returns)
# Send rights json back


class RightsAssembler(object):
    """Assembles and returns a list of rights statements."""

    def retrieve_rights(self, rights_ids):
        """Retrieves rights shells matching identifiers."""
        return [RightsShell.objects.get(pk=ident) for ident in rights_ids]

    def get_date_value(self, object, field_name, request_date, period):
        """Calculates the value for a date.

        Args:
            object (obj): the RightsShell or RightsGranted object for which a date is to be calculated.
            field_name (str): the object attribute containing date data.
            request_date (str): string representation of a date in ISO format.
            period (int): the number of years to be used in calculating the date.

        Returns:
            A date object representation of the date after calculation.
        """
        if not getattr(object, field_name):
            return datetime.strptime(request_date, "%Y-%m-%d").date() + relativedelta(years=period)
        else:
            return getattr(object, field_name) + relativedelta(years=period)

    def calculate_dates(self, object, request_start_date, request_end_date):
        """Calculate rights start and end dates for a given object.

        Args:
            object (obj): a RightsShell or RightsGranted object.
            request_start_date (string): the start date for a group of records.
            request_end_date (string): the end date for a group of records.

        Returns:
            object_start, object_end (tuple): a tuple with two datetime objects
                representing the group of object's start and end dates after
                calculation.
        """
        object_start = self.get_date_value(
            object, "start_date", request_start_date, object.start_date_period)
        object_end = None if object.end_date_open else self.get_date_value(
            object, "end_date", request_end_date, object.end_date_period)
        return object_start, object_end

    def create_json(self, obj, object_start, object_end):
        """docstring for create_json"""
        if obj.__class__.__name__ == "RightsShell":
            serializer = RightsShellSerializer(obj, context={"start_date": object_start, "end_date": object_end})
        else:
            serializer = RightsGrantedSerializer(obj, context={"start_date": object_start, "end_date": object_end})
        bytes = JSONRenderer().render(serializer.data)
        data = json.loads(bytes)
        return data

    def return_rights(self):
        """docstring for return_rights"""
    pass

    def run(self, rights_ids, request_start_date, request_end_date):
        """Assembles and returns rights statements given rights shell IDs and
        start and end dates.

        Args:
            rights_ids (list): a list of identifiers for rights shells.
            request_start_date (string): a string representation of the earliest date of a group of records
            request_end_date (string): a string representation of the latest date of a group of records
        """
        try:
            rights_shells = self.retrieve_rights(rights_ids)
            shell_data = []
            for shell in rights_shells:
                act_dates = []
                grant_data = []
                self.calculate_dates(shell, request_start_date, request_end_date)
                serialized_shell = self.create_json(shell, object_start, object_end)
                grants = shell.rightsgranted_set.all()
                for grant in grants:
                    act_dates.append(self.calculate_dates(grant, request_start_date, request_end_date))
                    serialized_grant = self.create_json(shell, object_start, object_end)
                    grant_data.append(serialized_grant)
                serialized_shell["rights_granted"].append(grant_data)
                shell_data.append(serialized_shell)

        except RightsShell.DoesNotExist as e:
            raise Exception("Error retrieving rights shell: {}".format(str(e)))
