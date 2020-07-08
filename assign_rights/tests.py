import random
import string
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .assemble import RightsAssembler
from .forms import GroupingForm
from .models import Grouping, RightsShell, User
from .views import (GroupingCreateView, GroupingDetailView, GroupingListView,
                    GroupingUpdateView, RightsAssemblerView)


def random_date():
    now = date.today()
    r = now - relativedelta(years=random.randint(2, 50))
    return r.isoformat()


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


def add_rights_shells(count=5):
    for x in range(count):
        RightsShell.objects.create(
            rights_basis=random.choice(["Copyright", "Statute", "License", "Other"]),
            copyright_status="copyrighted",
            determination_date=random_date(),
            note=random_string(),
            start_date=random_date(),
            end_date=random_date(),
            start_date_period=None,
            end_date_period=random.randint(0, 10),
            end_date_open=False,
            license_terms=None,
            statute_citation=None)


class TestViews(TestCase):

    def setUp(self):
        self.api_factory = APIRequestFactory()
        self.factory = RequestFactory()
        self.user = User.objects.create_user("test_user", "test@example.com", "testpass")
        add_rights_shells()
        add_groupings()

    def test_rightsassembler_pass(self):
        request = self.factory.post(reverse('rights-assemble'), {"identifiers": [1, 2, 3, 4], "end_date": "2020-03-01"}, format='json')
        response = RightsAssemblerView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_grouping_views(self):
        """Ensures that views are returning successful responses."""
        for view_str, view, pk_required in [
                ("groupings-list", GroupingListView, False),
                ("groupings-detail", GroupingDetailView, True),
                ("groupings-create", GroupingCreateView, False),
                ("groupings-update", GroupingUpdateView, True)]:
            pk = random.choice(Grouping.objects.all()).pk if pk_required else None
            request = self.factory.get(reverse(view_str, kwargs={"pk": pk})) if pk else self.factory.get(reverse(view_str))
            request.user = self.user
            response = view.as_view()(request, pk=pk) if pk else view.as_view()(request)
            self.assertEqual(response.status_code, 200)

    def test_grouping_form(self):
        form_data = {"title": random_string(10), "description": random_string(25), "rights_shells": [random.choice(RightsShell.objects.all())]}
        form = GroupingForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        for field in ["title", "description", "rights_shells"]:
            del form_data[field]
            form = GroupingForm(data=form_data)
            self.assertFalse(form.is_valid(), "Form unexpectedly valid")
            self.assertIsNot(
                form.errors[field], False,
                "Field-specific error message not raised for {}".format(field))


class TestRightsAssembler(TestCase):
    def setUp(self):
        add_rights_shells()
        self.assembler = RightsAssembler()

    def test_retrieve_rights(self):
        """Tests the retrieve_rights method.

        Asserts the method returns a list or DoesNotExist exception.
        """
        rights_ids = [obj.pk for obj in RightsShell.objects.all()]
        assembled = self.assembler.retrieve_rights(rights_ids)
        self.assertTrue(isinstance(assembled, list))
        self.assertEqual(len(rights_ids), len(assembled))

        deleted = random.choice(RightsShell.objects.all())
        deleted.delete()
        rights_ids.append(deleted.pk)
        with self.assertRaises(RightsShell.DoesNotExist):
            assembled = self.assembler.retrieve_rights(rights_ids)

    def test_calculate_dates(self):
        rights_ids = [obj.pk for obj in RightsShell.objects.all()]
        assembled = self.assembler.retrieve_rights(rights_ids)
        now = date.today()
        end_date = now - relativedelta(years=random.randint(2, 50))
        end_date.isoformat()
        for shell in assembled:
            dates = self.assembler.calculate_dates(shell, end_date)

class TestAssignRightsViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("test", "test@example.com", "testpass")
        self.factory = RequestFactory()
        add_groupings()

    def test_restricted_views(self):
        """Asserts that restricted views are only available to logged-in users."""
        restricted_views = [
            ("groupings-list", GroupingListView, None),
            ("groupings-detail", GroupingDetailView, random.choice(Grouping.objects.all()).pk),
            ("groupings-create", GroupingCreateView, False),
            ("groupings-update", GroupingUpdateView, random.choice(Grouping.objects.all()).pk)]
        for view_name, view, pk in restricted_views:
            request = self.factory.get(reverse(view_name, kwargs={"pk": pk})) if pk else self.factory.get(reverse(view_name))
            request.user = AnonymousUser()
            response = view.as_view()(request, pk=pk) if pk else view.as_view()(request)
            self.assertEqual(
                response.status_code, 302,
                "Restricted view {} available without authentication".format(view))

            request.user = self.user
            authenticated_response = view.as_view()(request, pk=pk) if pk else view.as_view()(request)
            self.assertEqual(
                authenticated_response.status_code, 200,
                "Restricted view {} not reachable by authenticated user".format(view))
