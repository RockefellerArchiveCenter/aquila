from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import User
from .views import LoggedInView


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
