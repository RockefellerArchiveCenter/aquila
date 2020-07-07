from django.core.exceptions import ObjectDoesNotExist
from .models import RightsShell

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
            try:
                rights_shells.append(RightsShell.objects.get(pk=ident))
            except RightsShell.DoesNotExist:
                error = "Could not find matching shell with identifier: {}".format(
                str(ident)
                )
                print(error)
        return rights_shells

    def calculate_dates(self, end_date):
        """docstring for calculate_dates"""
    pass

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
                self.calculate_dates(end_date)
        except Exception as e:
            print("Error retrieving rights shell: {}".format(str(e)))
