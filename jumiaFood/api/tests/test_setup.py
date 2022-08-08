from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import (
    Country,
    Business_Type
)
# from user.models import User


class TestSetUp(APITestCase):
    def setUp(self):
        self.country_url = reverse("country")
        self.business_type_url = reverse("business_type")
        self.country = Country.objects.create(country_name="country")
        self.business_Type = Business_Type.objects.create(type="type")

        self.country_data = {
            "country_name": "country"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
