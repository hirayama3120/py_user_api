from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from rest_framework.test import APITestCase

from ..models import Users

class TestUserListCreateAPIView(APITestCase):
    """ UserListCreateAPIViewのテストクラス """

    URL = '/api/users/'

    @classmethod
    def setUpClass(self):
        Users.objects.create(
            first_name='fname1', last_name='lname1', age=11, mail_address='test1@example.com'
        )
        Users.objects.create(
            first_name='fname2', last_name='lname2', age=22, mail_address='test2@example.com'
        )
        Users.objects.create(
            first_name='fname3', last_name='lname3', age=33, mail_address='test3@example.com'
        )


    def test_user_list_success(self):
        """ Usersモデルへの一覧取得APIへのGETリクエスト (正常系) """
        response = self.client.get(self.URL, format='json')

        self.assertEqual(response.status_code, 200)

        users = Users.objects.all()
        user1 = users[0]
        user2 = users[1]
        user3 = users[2]

        expected_json_dict = [
            {
                'id': user1.id,
                'first_name': user1.first_name,
                'last_name': user1.last_name,
                'age': user1.age,
                'mail_address': user1.mail_address,
                'delete_flag': user1.delete_flag,
                'created_add': str(localtime(user1.created_add)).replace(' ', 'T'),
                'updated_add': str(localtime(user1.updated_add)).replace(' ', 'T')
            },{
                'id': user2.id,
                'first_name': user2.first_name,
                'last_name': user2.last_name,
                'age': user2.age,
                'mail_address': user2.mail_address,
                'delete_flag': user2.delete_flag,
                'created_add': str(localtime(user2.created_add)).replace(' ', 'T'),
                'updated_add': str(localtime(user2.updated_add)).replace(' ', 'T')
            },{
                'id': user3.id,
                'first_name': user3.first_name,
                'last_name': user3.last_name,
                'age': user3.age,
                'mail_address': user3.mail_address,
                'delete_flag': user3.delete_flag,
                'created_add': str(localtime(user3.created_add)).replace(' ', 'T'),
                'updated_add': str(localtime(user3.updated_add)).replace(' ', 'T')
            }
        ]
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_success(self):
        """ Usersモデルへの登録APIへのPOSTリクエスト (正常系) """
        params = {
            "first_name": "first_name",
            "last_name": "last_name",
            "age": 99,
            "mail_address": "test_address@example.com"
        }
        before_user_count = Users.objects.count()

        response = self.client.post(self.URL, params, format='json')

        self.assertEqual(Users.objects.count(), before_user_count+1 )
        self.assertEqual(response.status_code, 201)
        user = Users.objects.latest('created_add')
        expected_json_dict = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'mail_address': user.mail_address,
            'delete_flag': False,
            'created_add': str(localtime(user.created_add)).replace(' ', 'T'),
            'updated_add': str(localtime(user.updated_add)).replace(' ', 'T')
        }
        self.assertJSONEqual(response.content, expected_json_dict)

        user.delete()

    @classmethod
    def tearDownClass(self):
        Users.objects.all().delete()