from .test_setup import TestSetUp
from ..models import (
    Country,
    Business_Type
)


class TestModels(TestSetUp):

    def test_country_model(self):
        country = self.country
        self.assertTrue(
            isinstance(
                country,
                Country
                )
            )
        self.assertEqual(
            str(country),
            '<Country: country'
            )

    def test_business_Type_model(self):
        business_Type = self.business_Type
        
        self.assertTrue(
            isinstance(
                business_Type,
                Business_Type
                )
            )
        self.assertEqual(
            str(business_Type),
            '<Business_Type: type'
            )
