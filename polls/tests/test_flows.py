# polls/tests/test_flows.py
from django.urls import reverse
from rest_framework.test import APITestCase
from polls.models import Poll, Option, Vote

class PollVotingFlowTests(APITestCase):
    def setUp(self):
        self.poll = Poll.objects.create(question="Best language?")
        self.option = Option.objects.create(poll=self.poll, text="Python")

    def test_create_poll_and_vote_once(self):
        url = reverse("vote-list")
        response = self.client.post(url, {"option": self.option.id}, format="json")
        self.assertEqual(response.status_code, 201)

        # Second vote in same session should fail
        response = self.client.post(url, {"option": self.option.id}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_new_session_allows_vote_again(self):
        url = reverse("vote-list")
        response = self.client.post(url, {"option": self.option.id}, format="json")
        self.assertEqual(response.status_code, 201)

        # Start a new session
        self.client.cookies.clear()
        response = self.client.post(url, {"option": self.option.id}, format="json")
        self.assertEqual(response.status_code, 201)

    def test_anonymous_delete_is_forbidden(self):
        # Create a vote first
        vote = Vote.objects.create(option=self.option, session_key="abc123")
        url = reverse("vote-detail", args=[vote.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
