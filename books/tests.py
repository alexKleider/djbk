from django.test import TestCase

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from books.views import home_page

import os
import shutil

from books.src.config import DEFAULTS as D
import books.src.entities as ents

cwd = os.getcwd()
temp_dir_name = os.path.join(cwd, "data.d")
original_dir_name = D["home"]

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

def get_decoded_content_of_response_to_a_POST(
                            view_func, key, submission):
    request = HttpRequest()
    request.method = "POST"
    request.POST[key] = submission
    response = view_func(request)
    return response.content.decode()

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

    def test_home_page_can_save_a_post_request(self):
        """
        creates returned2.txt and rendered2.txt
        and     returned3.txt and rendered3.txt
        """
        entity = "FirstEntity"
        request = HttpRequest()
        request.method = "POST"
        request.POST["new_entity"] = entity

        response = home_page(request)

        expected_html = render_to_string('home.html',
            {'new_entity_text': entity})
        content = response.content.decode()

        self.assertIn(entity, content)

        msg = send2files(content, expected_html, n=2)
        self.assertFalse(
            n_differing_lines(content, expected_html) > 1,
            msg + " differ by more than the 1 line")

        rendered_html = render_to_string('home.html') 
        returned_html = response.content.decode()

        msg = send2files(returned_html, rendered_html, n=3)
        self.assertFalse(
            n_differing_lines(returned_html ,rendered_html) > 1,
            msg + " differ by > 1 line")

    def test_home_page_can_save_a_post_request(self):
        """
        creates returned4.txt and rendered4.txt
        """
        new_item = "FirstEntity"

        content = get_decoded_content_of_response_to_a_POST(
            home_page, "new_entity", new_item)
        self.assertIn(new_item, content)

        expected_html = render_to_string('home.html',
            {'new_entity_text': new_item})

        msg = send2files(content, expected_html, n=4)
        self.assertFalse(
            n_differing_lines(content ,expected_html) > 1,
            msg + " differ by > 1 line.")

class PersistenceTest(TestCase):

    def setUp(self):
        os.rename(original_dir_name, temp_dir_name)
        os.mkdir(original_dir_name)
        file_name = os.path.join(original_dir_name, D['last_entity'])
        with open(file_name, 'w') as f_obj:
            f_obj.write('')
        shutil.copy(
            os.path.join(temp_dir_name, D['cofa_template']),
            D['home'])

    def tearDown(self):
        shutil.rmtree(original_dir_name)
        os.rename(temp_dir_name, original_dir_name)

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
        content = get_decoded_content_of_response_to_a_POST(
            home_page, "new_entity", entity1)
        content = get_decoded_content_of_response_to_a_POST(
            home_page, "new_entity", entity2)
        content = get_decoded_content_of_response_to_a_POST(
            home_page, "new_entity", entity3)
        self.assertIn("1. {}".format(entity1), content)
        self.assertIn("2. {}".format(entity2), content)
        self.assertIn("3. {}".format(entity3), content)


