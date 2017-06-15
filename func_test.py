#!../venv/bin/python

# File: func_test.py    (..in ~/Py/Djbk/debk)

# DON'T USE THIS FILE-
# USE INSTEAD f_tests/test.py

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

from selenium import webdriver

import unittest

class NewAccountTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_user_gets_to_opening_page(self):
        self.browser.get('http://localhost:8000')
#       self.assertIn("Django", self.browser.title)
        self.assertIn("Double Entry Book Keeping", self.browser.title)

    def test_user_choose_from_a_menu_to_create_an_entity(self):
        """
        She is presented with a menu with a choice to create an
        entity...:
        """
        inputbox = self.browser.find_element_by_id('id_user_id')
        self.assertEqual(inputbox.get_attribute('place_holder'),
            'Enter your user ID')
        inputbox

    def test_all_finished(self):
        self.fail("Finish tests!")

if __name__ == "__main__":
    unittest.main(warnings='ignore')
