from django.test import TestCase
# Create your tests here.
from.models import MyModel
from.views import show_login_page
    
class TestShowLoginPage(TestCase):
    def test_show_login_page(self):
        response = show_login_page(None)
        self.assertEqual(response.status_code, 200)