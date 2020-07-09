from dateutil.relativedelta import relativedelta

from .models import RightsShell

# Receive POST request that contains multiple rights IDs and one date
# For each rights ID, take date to calculate and return rights json (that looks like what Aurora returns)
# Send rights json back


class RightsAssembler(object):
    """Reads through a list of ids from a POST request and gets matching RightsShells
    for each identifier (matching against the primary key). Gets all RightsGranted
    objects related to each shell. Then, calculates rights end dates based on on info
    from the POST request or rights shells.
    """

    def retrieve_rights(self, rights_ids):
        """Retrieves a rights shell whose rights_id matches an identifier from
        a post request.
        """
        rights_shells = []
        for ident in rights_ids:
            rights_shells.append(RightsShell.objects.get(pk=ident))
        return rights_shells

    def calculate_dates(self, object, grouping_end_date):
        """Calculate rights end dates for a given object based on whether the end
        date is open, and then based on the period and end_dates in the object.

        If no end date in the object, use the grouping end date.
        """
        if not object.end_date_open:
            period = object.end_date_period
            if not object.end_date:
                object_end = grouping_end_date + relativedelta(years=period)
            else:
                object_end = object.end_date + relativedelta(years=period)
        else:
            object_end = None
        return object_end

    def create_json(self):
        """docstring for create_json"""
    pass

    def return_rights(self):
        """docstring for return_rights"""
    pass

    def run(self, rights_ids, grouping_end_date):
        try:
            rights_shells = self.retrieve_rights(rights_ids)
            for shell in rights_shells:
                act_dates = []
                self.calculate_dates(shell, grouping_end_date)
                grants = shell.rightsgranted_set.all()
                for grant in grants:
                    act_dates.append(self.calculate_dates(grant, grouping_end_date))

        except RightsShell.DoesNotExist as e:
            print("Error retrieving rights shell: {}".format(str(e)))
