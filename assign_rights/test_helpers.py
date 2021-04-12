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
    elif choice == 2:
        start_date = random_date(100, 25)
        end_date_period = random.randint(20, 75)
    elif choice == 3:
        start_date_period = random.randint(0, 10)
        end_date_period = random.randint(20, 75)
    else:
        start_date_period = random.randint(0, 10)
        end_date_open = True
    return start_date, end_date, start_date_period, end_date_period, end_date_open


def add_rights_shells(count=15):
    for x in range(count):
        start_date, end_date, start_date_period, end_date_period, end_date_open = set_dates()
        new_shell = RightsShell(determination_date=random_date(10, 0), note=random_string(), start_date=start_date, end_date=end_date, start_date_period=start_date_period, end_date_period=end_date_period, end_date_open=end_date_open)
        basis = random.choice(["copyright", "policy", "donor", "statute", "license"])
        new_shell.rights_basis = basis
        if basis in ["copyright", "statute"]:
            new_shell.jurisdiction = random.choice(["US", "us", "AU", "au"])
        if basis == "copyright":
            new_shell.copyright_status = random.choice(["copyrighted", "public domain", "unknown"])
        elif basis == "statute":
            new_shell.statute_citation = random_string()
        elif basis == "license":
            new_shell.license_terms = random_string()
        new_shell.save()


def add_rights_acts(count=5):
    for x in range(count):
        start_date, end_date, start_date_period, end_date_period, end_date_open = set_dates()
        RightsGranted.objects.create(
            basis=random.choice(RightsShell.objects.all()),
            act=random.choice(["publish", "disseminate", "replicate", "migrate", "modify", "use", "delete"]),
            restriction=random.choice(["allow", "disallow", "conditional"]),
            start_date=start_date,
            end_date=end_date,
            start_date_period=start_date_period,
            end_date_period=end_date_period,
            end_date_open=end_date_open,
        )
