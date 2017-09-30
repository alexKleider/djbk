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

def send2file(text, file_name):
    with open(file_name, 'w') as outfile:
        outfile.write(text)

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
            n_differing_lines(returned_html ,rendered_html) > 1,
            "returned_html and rendered_html differ by more than the 1 line")

    def test_home_page_can_save_a_post_request(self):
        entity = "FirstEntity"
        request = HttpRequest()
        request.method = "POST"
        request.POST["new_entity"] = entity

        response = home_page(request)
        content = response.content.decode()
        self.assertIn(entity, content)
        # v- putting input into the correct place.
        expected_html = render_to_string('home.html',
            {'new_entity_text': entity})

#       print('\n', content, '\n')
        send2file(content, 'content.txt')
        send2file(expected_html, 'expected.txt')
        self.assertFalse(
            n_differing_lines(content, expected_html) > 1,
            "content and expected html differ by more than the 1 line")

        returned_html = response.content.decode()
        rendered_html = render_to_string('home.html') 
        self.assertFalse(
            n_differing_lines(returned_html ,rendered_html) > 1,
            "returned and rendered differ by > 1 line")

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
        self.assertFalse(
            n_differing_lines(content ,expected_html) > 1,
            "Content and expected differ by > 1 line."
            )

