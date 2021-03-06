from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):

    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'testusername', 'password': 'testpassword'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('testusername'))
                self.assertDictEqual({'message': 'User created successfully'}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'testusername', 'password': 'testpassword'})
                auth_response = client.post('/auth', data=json.dumps({'username': 'testusername', 'password': 'testpassword'}),
                                           headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'testusername', 'password': 'testpassword'})

                response = client.post('/register', data={'username': 'testusername', 'password': 'testpassword'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'}, json.loads(response.data))


