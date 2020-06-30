# Receive POST request that contains multiple rights IDs and one date
# For each rights ID, take date to calculate and return rights json (that looks like what Aurora returns)
# Send rights json back


class RightsAssembler(object):
    """docstring for RightsCalculator"""

    def retrieve_rights(self, item):
        """docstring for retrieve_rights"""
        shell = RightsShell.objects.get(rights_id=id)
        return shell

    def calculate_dates(self):
        """docstring for calculate_dates"""
    pass

    def create_json(self):
        """docstring for create_json"""
    pass

    def return_rights(self):
        """docstring for return_rights"""
    pass

    def run(self, request_list):
        for item in request_list:
            self.retrieve_rights(item)
            return 'test'
