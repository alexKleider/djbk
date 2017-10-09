# File: books/tests.py

from django.test import TestCase

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from books.views import home_page

from books.src.config import DEFAULTS as D
import books.src.entities as ents
from setup_d.utilities import save_local_data, restore_local_data

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
    n = 0
    for l1, l2 in zipped:
        if l1 != l2:
            n += 1
    return n

def send2files(returned_txt, rendered_txt, n='', 
            returned_pattern = "returned{}.txt",
            rendered_pattern = "rendered{}.txt"):
    returned_file_name = returned_pattern.format(n)
    rendered_file_name = rendered_pattern.format(n)
    with open(returned_file_name, 'w') as outfile:
        outfile.write(returned_txt)
    with open(rendered_file_name, 'w') as outfile:
        outfile.write(rendered_txt)
    return "{} and {}".format(returned_file_name, rendered_file_name)

def get_response_to_a_POST(view_func, key, submission):
    request = HttpRequest()
    request.method = "POST"
    request.POST[key] = submission
    response = view_func(request)
    return response

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        creates returned1.txt and rendered1.txt
        """
        request = HttpRequest()
        response = home_page(request)
        returned_html = response.content.decode()
        rendered_html = render_to_string('home.html') 
        msg = send2files(returned_html, rendered_html, n=1)
        self.assertFalse(
            n_differing_lines(returned_html ,rendered_html) > 1,
            msg + " differ by more than the 1 line")

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        list_of_entities, _ = ents.get_file_info(D)
        self.assertEqual(len(list_of_entities), 0)

class PersistenceTest(TestCase):

    def setUp(self):
        save_local_data()

    def tearDown(self):
        restore_local_data()

    def test_home_page_can_save_a_POST_request(self):
        """
        """
        new_item = "FirstEntity"

        response = get_response_to_a_POST(
            home_page, "new_entity", new_item)
        
        content = response.content.decode()
        list_of_entities, _ = ents.get_file_info(D)

#       print("## Len: {}, new_item: {}, list: {}"
#           .format(len(list_of_entities),
#               new_item, list_of_entities))
        self.assertEqual(len(list_of_entities), 1)
        self.assertIn(new_item, list_of_entities)
#       self.assertIn(new_item, content)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_entity_persistence(self):
        entities, default = ents.get_file_info(D)
        self.assertTrue(len(entities) == 0)
        self.assertTrue(len(default) == 0)
        entity1 = "FirstEntity"
        ents.create_entity(entity1, D)
        entities, default = ents.get_file_info(D)
        self.assertTrue(len(entities) == 1)
        self.assertIn('FirstEntity', entities)

        entity2 = "SecondEntity"
        ents.create_entity(entity2, D)
        entities, default = ents.get_file_info(D)
        self.assertTrue(len(entities) == 2)
        self.assertIn('FirstEntity', entities)
        self.assertIn('SecondEntity', entities)

        entity3 = "ThirdEntity"
        ents.create_entity(entity3, D)
        entities, default = ents.get_file_info(D)
        self.assertTrue(len(entities) == 3)
        self.assertIn('FirstEntity', entities)
        self.assertIn('SecondEntity', entities)
        self.assertIn('ThirdEntity', entities)


    def test_entities_are_displayed(self):
        entity1 = "FirstEntity"
        entity2 = "SecondEntity"
        entity3 = "ThirdEntity"
        response = get_response_to_a_POST(
            home_page, "new_entity", entity1)
        response = get_response_to_a_POST(
            home_page, "new_entity", entity2)
        response = get_response_to_a_POST(
            home_page, "new_entity", entity3)
        content = response.content.decode()
#       self.assertIn("1. {}".format(entity1), content)
#       self.assertIn("2. {}".format(entity2), content)
#       self.assertIn("3. {}".format(entity3), content)


