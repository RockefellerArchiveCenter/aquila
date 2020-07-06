from .models import RightsShell

# Receive POST request that contains multiple rights IDs and one date
# For each rights ID, take date to calculate and return rights json (that looks like what Aurora returns)
# Send rights json back


class RightsAssembler(object):
    """docstring for RightsCalculator"""

    def retrieve_rights(self, item, shell_list):
        """docstring for retrieve_rights"""
        identifier = item.get("identifier")
        shell = RightsShell.objects.get(rights_id=identifier)
        shell_list.append(shell)
        return shell_list

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
        shell_list = []
        for item in request_list:
            try:
                self.retrieve_rights(item, shell_list)
            except Exception as e:
                print("Error retrieving rights shell: {}".format(str(e)))
        print(shell_list)
