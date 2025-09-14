from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from polls.models import Poll, Option, Vote

User = get_user_model()


class PollsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.poll = Poll.objects.create(question="Favorite color?")
        self.option1 = Option.objects.create(poll=self.poll, text="Red")
        self.option2 = Option.objects.create(poll=self.poll, text="Blue")

    # --- Root endpoint ---
    def test_api_root(self):
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('polls', response.data)
        self.assertIn('options', response.data)
        self.assertIn('votes', response.data)

    # --- Poll tests (CRUD) ---
    def test_list_polls(self):
        url = reverse('poll-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_poll_detail(self):
        url = reverse('poll-detail', args=[self.poll.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], self.poll.question)

    def test_create_poll(self):
        url = reverse('poll-list')
        data = {"question": "Best programming language?"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 2)

    def test_update_poll(self):
        url = reverse('poll-detail', args=[self.poll.id])
        data = {"question": "Updated color question?"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.question, "Updated color question?")

    def test_delete_poll(self):
        url = reverse('poll-detail', args=[self.poll.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Poll.objects.count(), 0)

    # --- Option tests (CRUD) ---
    def test_list_options(self):
        url = reverse('option-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)
        texts = [opt['text'] for opt in response.data]
        self.assertIn("Red", texts)
        self.assertIn("Blue", texts)

    def test_retrieve_option_detail(self):
        url = reverse('option-detail', args=[self.option1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], "Red")

    def test_create_option(self):
        url = reverse('option-list')
        data = {"poll": self.poll.id, "text": "Green"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Option.objects.count(), 3)

    def test_update_option(self):
        url = reverse('option-detail', args=[self.option1.id])
        data = {"poll": self.poll.id, "text": "Dark Red"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.option1.refresh_from_db()
        self.assertEqual(self.option1.text, "Dark Red")

    def test_delete_option(self):
        url = reverse('option-detail', args=[self.option1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Option.objects.count(), 1)

    # --- Vote tests ---
    def test_vote_requires_authentication(self):
        url = reverse('vote-list')
        response = self.client.post(url, {'option': self.option1.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_vote_authenticated(self):
        self.client.login(username='testuser', password='password')
        url = reverse('vote-list')
        response = self.client.post(url, {'option': self.option1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().user, self.user)

    def test_prevent_duplicate_vote(self):
        self.client.login(username='testuser', password='password')
        url = reverse('vote-list')
        # First vote
        self.client.post(url, {'option': self.option1.id})
        # Attempt duplicate vote in same poll
        response = self.client.post(url, {'option': self.option2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Vote.objects.count(), 1)

    def test_list_votes_authenticated(self):
        self.client.login(username='testuser', password='password')
        Vote.objects.create(user=self.user, option=self.option1)
        url = reverse('vote-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['option'], self.option1.id)

    def test_retrieve_vote_detail(self):
        self.client.login(username='testuser', password='password')
        vote = Vote.objects.create(user=self.user, option=self.option1)
        url = reverse('vote-detail', args=[vote.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['option'], self.option1.id)
