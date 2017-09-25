#!../venv/bin/python

FILE_NAME = "f_tests/test.py"

# The tests get run using ./manage.py test
# or ./manage.py test f_tests/test.py (if only want this one.)

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# User points browser to debk app, finds the site's home page
# which claims to provide 'Double Entry Book Keeping' infrastructure.

print('running {}'.format(FILE_NAME))

TEST_DATA_DIRECTORY = 'data/test-data'

import os
import shutil

class FirstVisitTest(LiveServerTestCase):
    
    def setUp(self):
        os.makedirs(TEST_DATA_DIRECTORY)
        self.browser = webdriver.Chrome()
        # self.browser.implicitly_wait(3)

    def tearDown(self):
        shutil.rmtree(TEST_DATA_DIRECTORY)
        self.browser.quit()
    
#   def test_check_tests_are_running(self):
        """ a 'smoke test' to check that tests are being run """
#       self.assertTrue(2 + 2 == 5)

    def test_data_dir_exists(self):
        os.path.isdir(TEST_DATA_DIRECTORY)

    def test_check_django_serving_our_site(self):
        self.browser.get('http://localhost:8000')
        title = self.browser.title
        self.assertIn('Double Entry Book Keeping', title)
        main_heading = (
            self.browser.find_element_by_tag_name(
                'h1').text)
        self.assertIn("SELECT or CREATE", main_heading)

# The home page provides a menu, one choice of which is to
# 0. Create a new accounting entity.
# so our user does just that:
        inbox = self.browser.find_element_by_id("id_new_entity")
        self.assertEqual(inbox.get_attribute('place_holder'),
            'Pick a name for your entity.')
# ..picks a name for a new entity:
        inbox.send_keys("FirstEntity")
        inbox.send_keys(Keys.ENTER)
# .. upon hitting enter, the 'FirstEntity' appears on the listing
# of already created entities.
        table = self.browser.find_element_by_id(
            "id_list_of_entities")
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertTrue(any(
            row.text == "FirstEntity" for row in rows))

        print("Expect the 'Finish the (functional) tests' error.")
        self.fail("Finish the tests.")
# She chooses to create a new entity and is presented with a
# new entity creation page containing a form
# into which she is asked to enter:
# 1.Business Name of Entity,
# 2.Folder Name of Entity,
# 3.SuperUser ID,
# 4 Possibly a list of authorized user IDs
# 5 Eventually add authentication.
# This page provides info as to naming of entities and does auto entry
# of folder name and does error checking (must be a valid path name.)
# No need to restrict entity names, only the folder names.

# She creates an entity: My New Company
# and after error checking, a 'my_new_company' folder is created.
# Error checking ensures that no duplication of folder names occurs by
# adding digit(s) if necessary.

# After entity creation she is shown its chart of accounts page
# where accounts can be created in one of two ways:
# 1.one at a time
#   check validity of each entry
# 2.offering a file
#   check validity
# OR user can finish account creation

# Work on an Exixting Entity
# Home page lists entities already created and user may choose one.
# User chooses an entity:
# - (gets validated)
# - gets taken to the entity's main page which offers the following
# choices:
#    1. journal entry- individual
#    2. journal entry- batch
#    3. Reports
#      a. balance sheet
#      b. journal
#    4. Adjustments
#      a. ....

# Depends on the dev server running.
# Functional Test==Acceptance Test==End-To-End Test==Black Box Test.
"""
A double entry book keeping system.

A user wants to use the system.
She checks out the url and sees that its title contains
"Double Entry Book Keeping" ...
She is prompted to enter her user name ...
^^^^^^ tested vs STILL TO TEST ...vvvv
She's never used the system before so:
She must set herself up with user name and password ...
And then create one or more Entities.
She can then choose to do book keeping for one of her entities.
Options:
1.  There will be an option to set up accounts, either one at a time
    or by selecting a text file (which will be accepted if formatted
    correctly and containing no conflicts.)
2.  Another option will be to make journal entries:
        each must have a date (set to currend date by default,)
        some descriptive text and
        at a minimum two line entries each containing
            an account number, a currency amount, and Dr or Cr.
        The amounts must balance out to 0.
3.  Examine records (journal &/or accounts) with option to print.
4.  End of fiscal period close out

"""
