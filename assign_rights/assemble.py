from .models import RightsShell

# Receive POST request that contains multiple rights IDs and one date
# For each rights ID, take date to calculate and return rights json (that looks like what Aurora returns)
# Send rights json back


class RightsAssembler(object):
    """docstring for RightsCalculator"""

    def retrieve_rights(self, identifier):
        """Retrieves a rights shell whose rights_id matches an identifier from
        a post request.
        """
        return RightsShell.objects.get(rights_id=identifier)

    def calculate_dates(self):
        """docstring for calculate_dates"""
    pass

    def create_json(self):
        """docstring for create_json"""
    pass

    def return_rights(self):
        """docstring for return_rights"""
    pass

    def run(self, rights_ids, end_date):
        shells = []
        for identifier in rights_ids:
            try:
                shells.append(self.retrieve_rights(identifier))
            except Exception as e:
                print("Error retrieving rights shell: {}".format(str(e)))
        print(shells)
