from dateutil.relativedelta import relativedelta

from .models import RightsGranted, RightsShell

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

    def calculate_dates(self, shell, grouping_end_date):
        """Calculate rights end dates for a given shell.

        If the shell's end date is not open, set the period to the shell's end date
        period. Then, if the shell doesn't have an applicable end date, make the shell's
        end date based on the POST end date. If it does have an applicable end date,
        calculate based on that value. If the shell's end date is open, return None.

        Get a queryset of all RightsGranted objects with foreign key relationships
        to the given shell.

        For each RightsGranted object in queryset, if grant end date is not open set
        the period to the end date period. If the grant does not have an end date, calculate
        act end date based on POST end date. Else, calculate the act end date based
        on the grant end date. If the grant's end date is open, return None, for no
        end date to the act.

        Return a structured dict with basis end date and associated act ids and end dates.
        """
        rights_info = {}
        grants_end = []
        if not shell.end_date_open:
            period = shell.end_date_period
            if not shell.applicable_end_date:
                shell_end = grouping_end_date + relativedelta(years=period)
            else:
                shell_end = shell.applicable_end_date + relativedelta(years=period)
        else:
            shell_end = None
        grants = shell.rightsgranted_set.all()
        for grant in grants:
            act = {}
            if not grant.end_date_open:
                period = grant.end_date_period
                if not grant.end_date:
                    act["grant_id"] = grant.pk
                    act["act_end"] = grouping_end_date + relativedelta(years=period)
                    grants_end.append(act)
                else:
                    act["grant_id"] = grant.pk
                    act["act_end"] = grant.end_date + relativedelta(years=period)
                    grants_end.append(act)
            else:
                act["grant_id"] = grant.pk
                act["act_end"] = None
        rights_info["shell_end"] = shell_end
        rights_info["acts"] = grants_end
        print(rights_info)
        return rights_info

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
                self.calculate_dates(shell, grouping_end_date)

        except RightsShell.DoesNotExist as e:
            print("Error retrieving rights shell: {}".format(str(e)))
