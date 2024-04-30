import random
from os.path import join

from django.contrib.auth.models import AnonymousUser, Group
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from aquila import settings

from .forms import GroupingForm, RightsShellForm
from .models import Grouping, RightsShell, User
from .test_helpers import add_groupings, add_rights_shells, random_string
from .views import (GroupingCreateView, GroupingDetailView, GroupingListView,
                    GroupingUpdateView, RightsShellCreateView,
                    RightsShellDetailView, RightsShellListView,
                    RightsShellUpdateView)

valid_data_fixture_dir = join(settings.BASE_DIR, 'fixtures', 'valid_requests')
invalid_data_fixture_dir = join(settings.BASE_DIR, 'fixtures', 'invalid_requests')


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
            "basis_note": random_string(),
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
