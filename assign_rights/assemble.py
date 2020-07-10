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

    def check_dates(self, object, field_name, request_date, period):
        """Checks object.field_name and returns a variable based on whether fields
        exist or not.
        """
        if not getattr(object, field_name):
            d = request_date + relativedelta(years=period)
            return d
        else:
            d = getattr(object, field_name) + relativedelta(years=period)
            return d

    def calculate_dates(self, object, request_start_date, request_end_date):
        """Calculate rights end dates for a given object based on whether the end
        date is open, and then based on the period and end_dates in the object.
        If no end date in the object, use the grouping end date.
        """
        start_period = object.start_date_period
        end_period = object.end_date_period
        object_start = self.check_dates(object, "start_date", request_start_date, start_period)
        if not object.end_date_open:
            object_end = self.check_dates(object, "end_date", request_end_date, end_period)
        elif object.end_date_open:
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
