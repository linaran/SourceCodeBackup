from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate

from .models import Tweet
from .views import TweetList


class Test(APITestCase):
    # def setUp(self):
    #     self.test_user = User.objects.create_user("test_user", "test@user.com", "12345")
    #
    # def test_create_tweet(self):
    #     self.setUp()
    #     self.client.login(username='test_user', password='12345')
    #
    #     url = reverse('faketweeter:list_tweets')
    #     data = {
    #         'tweet': "TEST TEST TEST",
    #         'date_published': "2016-12-05T11:11:00Z",
    #         'id': 160,
    #         'user': 'test_user'
    #     }
    #
    #     response = self.client.post(url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Tweet.objects.count(), 1)
    #     self.assertEqual(Tweet.objects.get().tweet, "TEST TEST TEST")

    def test_list_users(self):
        url = reverse('faketweeter:list_users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
