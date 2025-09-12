from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from polls.models import Poll, Option, Vote

User = get_user_model()

class PollsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.poll = Poll.objects.create(question="Favorite color?")
        self.option1 = Option.objects.create(poll=self.poll, text="Red")
        self.option2 = Option.objects.create(poll=self.poll, text="Blue")

    def test_list_polls(self):
        response = self.client.get('/api/polls/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vote_requires_authentication(self):
        response = self.client.post('/api/votes/', {'option': self.option1.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_vote_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/api/votes/', {'option': self.option1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().user, self.user)
