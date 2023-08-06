from django.urls import reverse
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    def login(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        url = reverse('user-signin')
        response = self.client.post(path=url, data=data, format='json')
        return response.json()
