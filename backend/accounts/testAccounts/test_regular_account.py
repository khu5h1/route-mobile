# app/testPosts.py

from django.test import TestCase
from accounts.models import RegularAccount


class TestNecessaryFields(TestCase):
    # This test will test all the minimum required fields to create a user
    def testPost(self):
        user = RegularAccount(
            username=9896765436)
        self.assertEqual(user.username, 9896765436)
