# File register/tests.py   (...in ~/Py/DjBk/debk/)

"""
Django's work flow:
1. an HTTP request comes in for a particular URL.
2. Django resolves to URL to a view function.
3. The view function processes the request and 
returns an HTTP response.
"""

from django.test import TestCase

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from register.views import home_page

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(
            response.content.startswith(b'<html>'))
        self.assertIn(
            b'<title>Double Entry Book Keeping</title>',
            response.content)
        self.assertTrue(
            response.content.strip().endswith(b'</html>'))

