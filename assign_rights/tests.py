import json
import random
from datetime import date, datetime
from os import listdir
from os.path import join

from aquila import settings
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AnonymousUser, Group
from django.test import RequestFactory, TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .assemble import RightsAssembler
from .forms import GroupingForm, RightsShellForm
from .models import Grouping, RightsGranted, RightsShell, User
from .serializers import RightsGrantedSerializer, RightsShellSerializer
from .test_helpers import (add_groupings, add_rights_acts, add_rights_shells,
                           random_date, random_string)
from .views import (GroupingCreateView, GroupingDetailView, GroupingListView,
                    GroupingUpdateView, RightsAssemblerView,
                    RightsShellCreateView, RightsShellDetailView,
                    RightsShellListView, RightsShellUpdateView)

valid_data_fixture_dir = join(settings.BASE_DIR, 'fixtures', 'valid_requests')
invalid_data_fixture_dir = join(settings.BASE_DIR, 'fixtures', 'invalid_requests')


class TestRightsAssemblyView(TransactionTestCase):
    """ Tests that require stable pks """

    reset_sequences = True

    def setUp(self):
        self.api_factory = APIRequestFactory()
        self.factory = RequestFactory()
        add_rights_shells()
        add_rights_acts()

    def test_rightsassembly_view(self):
        """Tests handling of expected returns as well as exceptions."""

        # RightsAssembler returns expected value
        for f in listdir(valid_data_fixture_dir):
            with open(join(valid_data_fixture_dir, f), 'r') as json_file:
                valid_data = json.load(json_file)
                request = self.factory.post(reverse("rights-assemble"), valid_data, content_type='application/json')
                response = RightsAssemblerView.as_view()(request)
                self.assertEqual(response.status_code, 200, "Request error: {}".format(response.data))

        # RightsAssembler throws an exception
        for fixture_name, message in [("invalid_rights_id.json", "Error retrieving rights shell: RightsShell matching query does not exist."), ("no_start_date.json", "Request data must contain 'identifiers', 'start_date' and 'end_date' keys.")]:
            with open(join(invalid_data_fixture_dir, fixture_name), 'r') as json_file:
                invalid_data = json.load(json_file)
                request = self.factory.post(reverse("rights-assemble"), invalid_data, content_type='application/json')
                response = RightsAssemblerView.as_view()(request)
                self.assertEqual(response.status_code, 500, "Request should have returned a 500 status code")
                self.assertEqual(response.data["detail"], message)


class TestViews(TestCase):

    def setUp(self):
        self.api_factory = APIRequestFactory()
        self.factory = RequestFactory()
        self.user = User.objects.create_user("test_user", "test@example.com", "testpass")
        self.group = Group.objects.get(name='edit')
        self.user.groups.add(self.group)
        add_rights_shells()
        add_groupings()

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
        """Tests form handles data correctly."""
        form_data = {
            "title": random_string(10),
            "description": random_string(25),
            "rights_shells": [random.choice(RightsShell.objects.all())]}
        form = GroupingForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        for field in ["title", "description", "rights_shells"]:
            del form_data[field]
            form = GroupingForm(data=form_data)
            self.assertFalse(form.is_valid(), "Form unexpectedly valid")
            self.assertIsNot(
                form.errors[field], False,
                "Field-specific error message not raised for {}".format(field))

    def test_rightshell_views(self):
        """Ensures that views are returning successful responses."""
        for view_str, view, pk_required in [
                ("rights-list", RightsShellListView, False),
                ("rights-detail", RightsShellDetailView, True),
                ("rights-create", RightsShellCreateView, False),
                ("rights-update", RightsShellUpdateView, True)]:
            pk = random.choice(RightsShell.objects.all()).pk if pk_required else None
            request = self.factory.get(reverse(view_str, kwargs={"pk": pk})) if pk else self.factory.get(reverse(view_str))
            request.user = self.user
            response = view.as_view()(request, pk=pk) if pk else view.as_view()(request)
            self.assertEqual(response.status_code, 200)

    def test_rightsshell_form(self):
        """Test form handles data correctly"""
        form_data = {
            "rights_basis": random.choice([b[0] for b in RightsShell.RIGHTS_BASIS_CHOICES]),
            "note": random_string(),
            "start_date_period": random.randint(0, 10),
            "end_date_period": random.randint(0, 10),
            "rights_begin": "start_date_period",
            "rights_end": "end_date_period",
        }
        form = RightsShellForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        for field in ["rights_basis"]:
            del form_data[field]
            form = RightsShellForm(data=form_data)
            self.assertFalse(form.is_valid(), "Form unexpectedly valid")
            self.assertIsNot(
                form.errors[field], False,
                "Field-specific error message not raised for {}".format(field))

    def test_restricted_views(self):
        """Asserts that restricted views are only available to logged-in users."""
        restricted_views = [
            ("groupings-list", GroupingListView, None),
            ("groupings-detail", GroupingDetailView, random.choice(Grouping.objects.all()).pk),
            ("groupings-create", GroupingCreateView, False),
            ("groupings-update", GroupingUpdateView, random.choice(Grouping.objects.all()).pk),
            ("rights-list", RightsShellListView, None),
            ("rights-detail", RightsShellDetailView, random.choice(RightsShell.objects.all()).pk),
            ("rights-create", RightsShellCreateView, False),
            ("rights-update", RightsShellUpdateView, random.choice(RightsShell.objects.all()).pk)]
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


class TestRightsAssembler(TestCase):
    def setUp(self):
        add_rights_shells()
        add_rights_acts(count=15)
        self.assembler = RightsAssembler()
        self.rights_ids = [obj.pk for obj in RightsShell.objects.all()]

    def test_run_method(self):
        """Tests the run method"""
        request_end_date = random_date(49, 0).isoformat()
        request_start_date = random_date(100, 50).isoformat()
        run = RightsAssembler().run(self.rights_ids, request_start_date, request_end_date)
        self.assertIsNot(False, run)

    def test_retrieve_rights(self):
        """Tests the retrieve_rights method.

        Asserts the method returns a list or DoesNotExist exception.
        """
        assembled = self.assembler.retrieve_rights(self.rights_ids)
        self.assertTrue(isinstance(assembled, list))
        self.assertEqual(len(self.rights_ids), len(assembled))

        deleted = random.choice(RightsShell.objects.all())
        deleted.delete()
        self.rights_ids.append(deleted.pk)
        with self.assertRaises(RightsShell.DoesNotExist):
            assembled = self.assembler.retrieve_rights(self.rights_ids)

    def check_object_dates(self, object, request_start_date, request_end_date):
        """Tests different cases for date calculation.

        Asserts the method returns a DateTimeField or None if the end date is open.
        Asserts that the relative delta of the calculated date and the correct end date
        is equal to the end date period of the object.
        """
        start_date, end_date = self.assembler.get_dates(object, request_start_date, request_end_date)
        self.assertTrue(isinstance(start_date, date))
        if object.end_date_open:
            self.assertEqual(end_date, None)
        else:
            self.assertTrue(isinstance(end_date, date))

        if object.start_date_period:
            self.assertEqual(relativedelta(start_date, datetime.strptime(request_start_date, "%Y-%m-%d").date()).years, object.start_date_period)
        if object.end_date_period:
            self.assertEqual(relativedelta(end_date, datetime.strptime(request_end_date, "%Y-%m-%d").date()).years, object.end_date_period)

    def test_get_dates(self):
        """Tests the get_dates method."""
        shell = random.choice(RightsShell.objects.all())
        request_end_date = random_date(49, 0).isoformat()
        request_start_date = random_date(100, 50).isoformat()
        self.check_object_dates(shell, request_start_date, request_end_date)

        for granted in shell.rightsgranted_set.all():
            self.check_object_dates(granted, request_start_date, request_end_date)

    def test_create_json(self):
        """Tests that Serialzers are working as expected."""
        for obj_cls, serializer_cls in [
                (RightsShell, RightsShellSerializer),
                (RightsGranted, RightsGrantedSerializer)]:
            obj = random.choice(obj_cls.objects.all())
            start_date = random_date(75, 50).isoformat()
            end_date = random_date(49, 5).isoformat()
            serialized = self.assembler.create_json(obj, serializer_cls, start_date, end_date)
            self.assertTrue(isinstance(serialized, dict))
            self.assertEqual(start_date, serialized["start_date"])
            self.assertEqual(end_date, serialized["end_date"])
