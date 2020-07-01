from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .assemble import RightsAssembler
from .views import RightsAssemblerView

class TestViews(TestCase):

    def test_rightsassemblerview(self):
        factory = APIRequestFactory()
        request = factory.post(reverse('rights-assemble'), {"items": [1,2,3]}, format='json')
        response = RightsAssemblerView.as_view()(request)
