from django.test import TestCase

# Create your tests here.

class SmokeTest(TestCase):

    def test_bad_math(self):
        print("Expect the 'bad_math' assertion error.")
        self.assertEqual(1 + 1, 3)

