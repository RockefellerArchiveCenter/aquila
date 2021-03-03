import random
import string
from datetime import date

from dateutil.relativedelta import relativedelta

from .models import Grouping, RightsGranted, RightsShell


def random_date():
    now = date.today()
    r = now - relativedelta(years=random.randint(2, 50))
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


def add_rights_shells(count=15):
    for x in range(count):
        RightsShell.objects.create(
            rights_basis=random.choice([b[0] for b in RightsShell.RIGHTS_BASIS_CHOICES]),
            copyright_status="copyrighted",
            determination_date=random_date(),
            note=random_string(),
            start_date=random.choice([None, random_date()]),
            end_date=random.choice([None, random_date()]),
            start_date_period=random.randint(0, 10),
            end_date_period=random.randint(0, 10),
            end_date_open=random.choice([True, False]),
            license_terms=None,
            statute_citation=None)


def add_rights_acts(count=5):
    for x in range(count):
        RightsGranted.objects.create(
            basis=random.choice(RightsShell.objects.all()),
            act=random.choice(["publish", "disseminate", "replicate", "migrate", "modify", "use", "delete"]),
            restriction=random.choice(["allow", "disallow", "conditional"]),
            start_date=random.choice([None, random_date()]),
            end_date=random.choice([None, random_date()]),
            start_date_period=random.randint(0, 10),
            end_date_period=random.randint(0, 10),
            end_date_open=random.choice([True, False]),
        )
