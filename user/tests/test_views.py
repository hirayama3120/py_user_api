from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Users

class TestUserListCreateAPIView(APITestCase):
    """ UserListCreateAPIViewのテストクラス """

    URL = '/api/users/'

    def test_create_success(self):
        """ Usersモデルへの登録APIへのPOSTリクエスト """
        params = {
            "first_name": "first_name",
            "last_name": "last_name",
            "age": 11,
            "mail_address": "test_address@example.com"
        }
        response = self.client.post(self.URL, params, format='json')

        self.assertEqual(Users.objects.count(), 1)
        self.assertEqual(response.status_code, 201)
        user = Users.objects.get()
        expected_json_dict = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'mail_address': user.mail_address
        }
        self.assertJSONEqual(response.content, expected_json_dict)
