from .test_setup import TestSetUp

class TestViews(TestSetUp):

    def test_country_cannot_be_added(self):
        res = self.client.post(self.country_url)
    
        self.assertEqual(res.status_code,400)
    
    def test_country_can_be_added(self):
        res = self.client.post(self.country_url,self.country_data,format="json")
  
        self.assertEqual(res.data["country_name"],self.country_data["country_name"])
        self.assertEqual(res.status_code,200)
        