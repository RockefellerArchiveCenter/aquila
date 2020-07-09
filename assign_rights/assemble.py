from dateutil.relativedelta import relativedelta

from .models import RightsGranted, RightsShell

# Receive POST request that contains multiple rights IDs and one date
# For each rights ID, take date to calculate and return rights json (that looks like what Aurora returns)
# Send rights json back


class RightsAssembler(object):
    """docstring for RightsCalculator"""

    def retrieve_rights(self, rights_ids):
        """Retrieves a rights shell whose rights_id matches an identifier from
        a post request.
        """
        rights_shells = []
        for ident in rights_ids:
            rights_shells.append(RightsShell.objects.get(pk=ident))
        return rights_shells

    def calculate_dates(self, shell, end_date):
        """docstring for calculate_dates"""
        rights_info = {}
        grants_end = []
        if not shell.end_date_open:
            period = shell.end_date_period
            if not shell.applicable_end_date:
                shell_end = end_date + relativedelta(years=period)
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
                    act["act_end"] = end_date + relativedelta(years=period)
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

    def run(self, rights_ids, end_date):
        try:
            rights_shells = self.retrieve_rights(rights_ids)
            for shell in rights_shells:
                self.calculate_dates(shell, end_date)

        except RightsShell.DoesNotExist as e:
            print("Error retrieving rights shell: {}".format(str(e)))
