import random
import string
from datetime import date

from dateutil.relativedelta import relativedelta

from .models import Grouping, RightsGranted, RightsShell


def random_date(earliest, latest):
    """Takes a range of years from today's date and returns a random date.

    Args:
    earliest (integer): start of range to pick a random integer from
    latest (integer): end of range to pick a random integer from
    """
    now = date.today()
    r = now - relativedelta(years=random.randint(latest, earliest))
    return r


def random_string(length=20):
    """Returns a random string of specified length."""
    return "".join(random.choice(string.ascii_letters) for m in range(length))


def add_groupings(count=5):
    for x in range(count):
        grouping = Grouping.objects.create(
            title=random_string(10),
            description=random_string(50))
        if RightsShell.objects.all():
            for x in range(random.randint(1, 3)):
                grouping.rights_shells.add(random.choice(RightsShell.objects.all()))


def set_dates():
    """Returns start and end dates in a way consistent with what is allowed in forms"""
    start_date = None
    end_date = None
    start_date_period = None
    end_date_period = None
    end_date_open = False
    choice = random.randrange(1, 5)
    if choice == 1:
        start_date = random_date(100, 25)
        end_date = random_date(24, -50)
    if choice == 2:
        start_date = random_date(100, 25)
        end_date_period = random.randint(20, 75)
    if choice == 3:
        start_date_period = random.randint(0, 10)
        end_date_period = random.randint(20, 75)
    else:
        start_date_period = random.randint(0, 10)
        end_date_open = True
    return start_date, end_date, start_date_period, end_date_period, end_date_open


def add_rights_shells(count=15):
    def copyright_shell():
        date_info = set_dates()
        RightsShell.objects.create(
            rights_basis="copyright",
            copyright_status=random.choice(["copyrighted", "public domain", "unknown"]),
            jurisdiction="us",
            determination_date=random_date(10, 0),
            note=random_string(),
            start_date=date_info[0],
            end_date=date_info[1],
            start_date_period=date_info[2],
            end_date_period=date_info[3],
            end_date_open=date_info[4],
        )

    def other_shell():
        date_info = set_dates()
        RightsShell.objects.create(
            rights_basis=random.choice(["policy", "donor"]),
            determination_date=random_date(10, 0),
            note=random_string(),
            start_date=date_info[0],
            end_date=date_info[1],
            start_date_period=date_info[2],
            end_date_period=date_info[3],
            end_date_open=date_info[4],
        )

    def statute_shell():
        date_info = set_dates()
        RightsShell.objects.create(
            rights_basis="statute",
            jurisdiction="us",
            determination_date=random_date(10, 0),
            note=random_string(),
            start_date=date_info[0],
            end_date=date_info[1],
            start_date_period=date_info[2],
            end_date_period=date_info[3],
            end_date_open=date_info[4],
            statute_citation=random_string(),
        )

    def license_shell():
        date_info = set_dates()
        RightsShell.objects.create(
            rights_basis="license",
            jurisdiction="us",
            determination_date=random_date(10, 0),
            note=random_string(),
            start_date=date_info[0],
            end_date=date_info[1],
            start_date_period=date_info[2],
            end_date_period=date_info[3],
            end_date_open=date_info[4],
            license_terms=random_string(),
        )

    shell_types = [copyright_shell, other_shell, statute_shell, license_shell]
    for x in range(count):
        random.choice(shell_types)()


def add_rights_acts(count=5):
    for x in range(count):
        date_info = set_dates()
        RightsGranted.objects.create(
            basis=random.choice(RightsShell.objects.all()),
            act=random.choice(["publish", "disseminate", "replicate", "migrate", "modify", "use", "delete"]),
            restriction=random.choice(["allow", "disallow", "conditional"]),
            start_date=date_info[0],
            end_date=date_info[1],
            start_date_period=date_info[2],
            end_date_period=date_info[3],
            end_date_open=date_info[4],
        )
