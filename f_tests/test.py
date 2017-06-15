#!../venv/bin/python

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# User points browser to debk app, finds the site's home page
# which claims to provide 'Double Entry Book Keeping' infrastructure.

class FirstVisitTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        # self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_django_is_running(self):
        content = self.browser.content()
        self.assertIn('Django', content)

# The home page provides a menu, one choice of which is to
# 0. Create a new accounting entity.
# Other choices are:
# 1. Work on an existing entity.

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
