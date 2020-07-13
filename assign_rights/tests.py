import random
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .assemble import RightsAssembler
from .forms import GroupingForm
from .models import Grouping, RightsShell, User
from .test_helpers import (add_groupings, add_rights_acts, add_rights_shells,
                           random_date, random_string)
from .views import (GroupingCreateView, GroupingDetailView, GroupingListView,
                    GroupingUpdateView)


class TestViews(TestCase):

    def setUp(self):
        self.api_factory = APIRequestFactory()
        self.factory = RequestFactory()
        self.user = User.objects.create_user("test_user", "test@example.com", "testpass")
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
        add_rights_acts()
        self.assembler = RightsAssembler()
        self.rights_ids = [obj.pk for obj in RightsShell.objects.all()]

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
        object.end_date_open = False
        object.start_date = random_date()
        object.end_date = random_date()
        start_date, end_date = self.assembler.calculate_dates(object, request_start_date, request_end_date)
        self.assertEqual(relativedelta(start_date, object.start_date).years, object.start_date_period)
        self.assertTrue(isinstance(start_date, date))
        self.assertEqual(relativedelta(end_date, object.end_date).years, object.end_date_period)
        self.assertTrue(isinstance(end_date, date))

        object.start_date = None
        object.end_date = None
        start_date, end_date = self.assembler.calculate_dates(object, request_start_date, request_end_date)
        self.assertEqual(relativedelta(
            start_date,
            date.fromisoformat(request_start_date)).years,
            object.start_date_period
        )
        self.assertTrue(isinstance(start_date, date))
        self.assertEqual(relativedelta(
            end_date,
            date.fromisoformat(request_end_date)).years,
            object.end_date_period
        )
        self.assertTrue(isinstance(end_date, date))

        object.end_date_open = True
        start_date, end_date = self.assembler.calculate_dates(object, request_start_date, request_end_date)
        self.assertEqual(end_date, None)

    def test_calculate_dates(self):
        """Tests the calculate_dates method."""
        shell = random.choice(RightsShell.objects.all())
        request_end_date = random_date().isoformat()
        request_start_date = random_date().isoformat()
        self.check_object_dates(shell, request_start_date, request_end_date)

        for granted in shell.rightsgranted_set.all():
            self.check_object_dates(granted, request_start_date, request_end_date)


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
