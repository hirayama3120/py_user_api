from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from rest_framework.test import APITestCase

from ..models import Users

class TestUserListCreateAPIView(APITestCase):
    """ UserListCreateAPIViewのテストクラス """

    URL = '/api/users/'

    def test_user_list_success(self):
        """ Usersモデルへの一覧取得APIへのGETリクエスト (正常系: 取得件数0件) """

        # テスト用Userオブジェクト登録
        for i in range(3):
            Users.objects.create(
                first_name=f'fname{i}',
                last_name=f'lname{i}',
                age=i,
                mail_address=f'test{i}@example.com'
            )

        # レスポンス期待値
        expected_json = []
        users = Users.objects.all()

        for i in range(len(users)):
            user = users[i]
            user_json = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'mail_address': user.mail_address,
                'delete_flag': user.delete_flag,
                'created_add': str(localtime(user.created_add)).replace(' ', 'T'),
                'updated_add': str(localtime(user.updated_add)).replace(' ', 'T')
            }
            expected_json.append(user_json)

        # APIリクエスト実行
        response = self.client.get(self.URL, format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_user_list_success_with_user_count_0(self):
        """ Usersモデルへの一覧取得APIへのGETリクエスト (正常系: 取得件数0件) """
        # レスポンス期待値
        expected_json = []

        # APIリクエスト実行
        response = self.client.get(self.URL, format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_create_success(self):
        """ Usersモデルへの登録APIへのPOSTリクエスト (正常系) """
        # 登録User情報
        first_name = "test_first_name"
        last_name = "test_last_name"
        age = 99
        mail_address = "test_address@example.com"

        # リクエストパラメーター
        params = {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "mail_address": mail_address
        }

        # 実行前登録件数
        before_user_count = Users.objects.count()

        # APIリクエスト実行
        response = self.client.post(self.URL, params, format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)

        user = Users.objects.latest('created_add')
        expected_json = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'mail_address': user.mail_address,
            'delete_flag': False,
            'created_add': str(localtime(user.created_add)).replace(' ', 'T'),
            'updated_add': str(localtime(user.updated_add)).replace(' ', 'T')
        }
        self.assertJSONEqual(response.content, expected_json)

        # データベースの状態を検証
        self.assertEqual(Users.objects.count(), before_user_count+1)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.age, age)
        self.assertEqual(user.mail_address, mail_address)

    def tearDown(self):
        Users.objects.all().delete()