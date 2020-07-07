from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .models import RightsShell
from .views import RightsAssemblerView


class TestViews(TestCase):

    def setUp(self):
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

    def test_rightsassemblerview(self):
        factory = APIRequestFactory()
        request = factory.post(reverse('rights-assemble'), {"identifiers": [1, 2, 3, 4], "end_date": "2020-03-01"}, format='json')
        response = RightsAssemblerView.as_view()(request)
