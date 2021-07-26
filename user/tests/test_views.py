from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from rest_framework.test import APITestCase

from ..models import Users

class TestUserListCreateAPIView(APITestCase):
    """ UserListCreateAPIViewのテストクラス """

    URL = '/api/users/'

    def test_user_list_success(self):
        """ Usersモデルへの一覧取得APIへのGETリクエスト (正常系: 取得件数3件) """
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

    def test_create_bad_request(self):
        """ Usersモデルへの登録APIへのPOSTリクエスト (異常系: バリデーションNG) """
        # リクエストパラメーター
        params = {
            "first_name": "0123456789_0123456789_0123456789_",
            "last_name": "test_last_name",
            "age": 99,
            "mail_address": "test_address@example.com"
        }

        # 実行前登録件数
        before_user_count = Users.objects.count()

        # APIリクエスト実行
        response = self.client.post(self.URL, params, format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

        # データベースの状態を検証
        self.assertEqual(Users.objects.count(), before_user_count)

class TestUserRetrieveUpdateDeleteAPIView(APITestCase):
    """ UserListCreateAPIViewのテストクラス """

    URL = '/api/users/{}/'

    @classmethod
    def setUpClass(self):
        super().setUpClass()

        self.user1 = Users.objects.create(
            first_name=f'fname1',
            last_name=f'lname1',
            age=1,
            mail_address=f'test1@example.com'
        )

        self.user2 = Users.objects.create(
            first_name=f'fname2',
            last_name=f'lname2',
            age=2,
            mail_address=f'test2@example.com'
        )

        self.user3 = Users.objects.create(
            first_name=f'fname3',
            last_name=f'lname3',
            age=3,
            mail_address=f'test3@example.com'
        )

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()

    def test_get_user_success(self):
        """ Usersモデルへの指定User取得APIへのGETリクエスト (正常系) """
        # レスポンス期待値
        user = Users.objects.get(pk=self.user3.id)

        expected_json = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'mail_address': user.mail_address,
            'delete_flag': user.delete_flag,
            'created_add': str(localtime(user.created_add)).replace(' ', 'T'),
            'updated_add': str(localtime(user.updated_add)).replace(' ', 'T')
        }

        # APIリクエスト実行
        response = self.client.get(self.URL.format(user.id), format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_json)

    def test_get_user_not_found(self):
        """ Usersモデルへの指定User取得APIへのGETリクエスト (異常系) """

        # APIリクエスト実行
        response = self.client.get(self.URL.format(999), format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 404)

    def test_put_user_success(self):
        """ Usersモデルへの指定User更新APIへのPUTリクエスト (正常系) """
        # レスポンス期待値
        user = Users.objects.get(pk=self.user3.id)

        request_json = expected_json = {
            'id': user.id,
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'age': user.age,
            'mail_address': user.mail_address,
            'delete_flag': user.delete_flag,
            'created_add': str(localtime(user.created_add)).replace(' ', 'T'),
            'updated_add': str(localtime(user.updated_add)).replace(' ', 'T')
        }

        # APIリクエスト実行
        response = self.client.put(self.URL.format(user.id), request_json, format='json')

        after_user = Users.objects.get(pk=self.user3.id)
        expected_json['updated_add'] = str(localtime(after_user.updated_add)).replace(' ', 'T')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content, expected_json)

    def test_put_user_not_found(self):
        """ Usersモデルへの指定User更新APIへのPUTリクエスト (異常系) """
        request_json = {}

        # APIリクエスト実行
        response = self.client.put(self.URL.format(999), request_json, format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 404)

    def test_delete_user_success(self):
        """ Usersモデルへの指定User削除APIへのDELETEリクエスト (正常系) """
        user = Users.objects.get(pk=self.user3.id)

        before_user_count = Users.objects.filter(delete_flag=False).count()

        # APIリクエスト実行
        response = self.client.delete(self.URL.format(user.id), format='json')

        after_user_count = Users.objects.filter(delete_flag=False).count()

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertEqual(before_user_count - 1, after_user_count)

    def test_delete_user_not_found(self):
        """ Usersモデルへの指定User更新APIへのPUTリクエスト (異常系) """
        # APIリクエスト実行
        response = self.client.delete(self.URL.format(999, format='json'))

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 404)