from dateutil.relativedelta import relativedelta

from .models import RightsShell

# Receive POST request that contains multiple rights IDs and one date
# For each rights ID, take date to calculate and return rights json (that looks like what Aurora returns)
# Send rights json back


class RightsAssembler(object):
    """Reads through a list of ids from a POST request and gets matching RightsShells
    for each identifier (matching against the primary key). Gets all RightsGranted
    objects related to each shell. Then, calculates rights start and end dates based
    on variables passed in from the POST request or rights shells.
    """

    def retrieve_rights(self, rights_ids):
        """Retrieves a rights shell whose rights_id matches an identifier from
        a post request.
        """
        rights_shells = []
        for ident in rights_ids:
            rights_shells.append(RightsShell.objects.get(pk=ident))
        return rights_shells

    def calculate_dates(self, object, request_start_date, request_end_date):
        """Calculate rights start and end dates for a given object.

        If there is no start date, use the start date from the request for calculations.
        Otherwise, use the object's start date.

        If the object's end date is open, return None.

        If the object doesn't have an end date, use the end date from the request.
        Otherwise, use the object's end date.
        """
        start_period = object.start_date_period
        end_period = object.end_date_period
        object_start = request_start_date + relativedelta(years=start_period)
        object_end = request_end_date + relativedelta(years=end_period)
        if object.start_date:
            object_start = object.start_date + relativedelta(years=start_period)
        if not object.end_date_open:
            if object.end_date:
                object_end = object.end_date + relativedelta(years=end_period)
        if object.end_date_open:
            object_end = None
        return object_start, object_end

    def create_json(self):
        """docstring for create_json"""
    pass

    def return_rights(self):
        """docstring for return_rights"""
    pass

    def run(self, rights_ids, request_start_date, request_end_date):
        try:
            rights_shells = self.retrieve_rights(rights_ids)
            for shell in rights_shells:
                act_dates = []
                self.calculate_dates(shell, request_start_date, request_end_date)
                grants = shell.rightsgranted_set.all()
                for grant in grants:
                    act_dates.append(self.calculate_dates(grant, request_start_date, request_end_date))

        except RightsShell.DoesNotExist as e:
            print("Error retrieving rights shell: {}".format(str(e)))
