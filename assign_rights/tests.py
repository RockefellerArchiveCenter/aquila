import random
import string
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .assemble import RightsAssembler
from .models import RightsShell, User
from .views import LoggedInView, RightsAssemblerView


def random_date():
    now = date.today()
    r = now - relativedelta(years=random.randint(2, 50))
    return r.isoformat()


def random_string(length=20):
    """Returns a random string of specified length."""
    return "".join(random.choice(string.ascii_letters) for m in range(length))


class TestViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        return RightsShell.objects.create(
            rights_id=1,
            rights_basis="Copyright",
            copyright_status="copyrighted",
            determination_date="2020-01-01",
            note="note",
            applicable_start_date="2019-02-01",
            applicable_end_date="2019-03-01",
            start_date_period=None,
            end_date_period=None,
            end_date_open=False,
            license_terms=None,
            statute_citation=None
        )

    def test_rightsassembler_pass(self):
        request = self.factory.post(reverse('rights-assemble'), {"identifiers": [1, 2, 3, 4], "end_date": "2020-03-01"}, format='json')
        response = RightsAssemblerView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestRightsAssembler(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        for x in range(5):
            RightsShell.objects.create(
                rights_id=random.randint(1, 10),
                rights_basis=random.choice(["Copyright", "Statute", "License", "Other"]),
                copyright_status="copyrighted",
                determination_date=random_date(),
                note=random_string(),
                applicable_start_date=random_date(),
                applicable_end_date=random_date(),
                start_date_period=None,
                end_date_period=random.randint(0, 10),
                end_date_open=False,
                license_terms=None,
                statute_citation=None
            )
            self.assembler = RightsAssembler()

    def test_retrieve_rights(self):
        """Tests the retrieve_rights method.

        Asserts the method returns a list or DoesNotExist exception.
        """
        rights_ids = [obj.pk for obj in RightsShell.objects.all()]
        assembled = self.assembler.retrieve_rights(rights_ids)
        self.assertTrue(isinstance(assembled, list))
        self.assertEqual(len(rights_ids), len(assembled))

        rights_ids.append(len(rights_ids) + 1)
        with self.assertRaises(RightsShell.DoesNotExist):
            assembled = self.assembler.retrieve_rights(rights_ids)


class TestAssignRightsViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("test", "test@example.com", "testpass")
        self.factory = RequestFactory()

    def test_restricted_views(self):
        """Asserts that restricted views are only available to logged-in users."""
        restricted_views = [("logged-in", LoggedInView)]
        for view_name, view in restricted_views:
            request = self.factory.get(reverse(view_name))
            request.user = AnonymousUser()
            response = LoggedInView.as_view()(request)
            self.assertEqual(
                response.status_code, 302,
                "Restricted view {} available without authentication".format(view))

            request.user = self.user
            authenticated_response = LoggedInView.as_view()(request)
            self.assertEqual(
                authenticated_response.status_code, 200,
                "Restricted view {} not reachable by authenticated user".format(view))
