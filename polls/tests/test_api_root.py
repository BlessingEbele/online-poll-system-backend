# polls/tests/test_api_root.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


class APIRootTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_root_response_matches_example(self):
        """
        Ensure api_root returns exactly what is documented in APIRootSerializer + examples.
        """
        response = self.client.get(reverse("api-root"))
        self.assertEqual(response.status_code, 200)

        # The documented example in extend_schema
        expected = {
            "polls": "http://testserver" + reverse("poll-list"),
            "options": "http://testserver" + reverse("option-list"),
            "votes": "http://testserver" + reverse("vote-list"),
        }

        self.assertEqual(response.json(), expected)
