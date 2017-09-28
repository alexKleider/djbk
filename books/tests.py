from django.test import TestCase

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from books.views import home_page

# Create your tests here.

unnecessary = """
class SmokeTest(TestCase):

    def test_bad_math(self):
        print("Expect the 'bad_math' assertion error.")
        self.assertEqual(1 + 1, 3)
"""

def n_differing_lines(s1, s2):
    """
    A helper function- returns the number of
    differing lines in the two string params.
    Solves for me the problem that
    django.template.loader.render_to_string
    does not render the {% csrf_token %}.
    Fails only if more than one line differs.
    """
    zipped = zip(s1.split("\n"), s2.split("\n"))
    n_differing_lines = 0
    for l1, l2 in zipped:
        if l1 != l2:
            n_differing_lines += 1
    return n_differing_lines

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):

        request = HttpRequest()
        response = home_page(request)
        returned_html = response.content.decode()
        rendered_html = render_to_string('home.html') 
        self.assertFalse(
            n_differing_lines(returned_html ,rendered_html) > 1)

    def test_home_page_can_save_a_post_request(self):
        new_item = "FirstEntity"

        request = HttpRequest()
        request.method = "POST"
        request.POST["new_entity"] = new_item

        response = home_page(request)
        content = response.content.decode()
        self.assertIn(new_item, content)
        # v- putting input into the correct place.
        expected_html = render_to_string('home.html',
            {'new_entity_text': new_item})

#       print('\n', content, '\n')
        self.assertEqual(content, expected_html)

