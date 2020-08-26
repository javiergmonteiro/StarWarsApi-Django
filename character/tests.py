from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from pprint import pprint


class CharacterTests(APITestCase):

    def test_post_rating(self):

        print("Testing: Posting rating for character 1 with value of 9\n")

        data = {'character':1,'rating':9}
        response = self.client.post("/character/1/rating/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        pprint(response.json())
        print()

    def test_get_character(self):

        print("Testing: Getting data from character 1\n")

        response = self.client.get("/character/1/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pprint(response.json())
        print()
    
