from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('user', 'password').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'user', 'password': 'password'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.header = {'Authorization': f'JWT {auth_token}'}

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # UserModel('user', 'password').save_to_db()
                # auth_request = client.post('/auth',
                #                            data=json.dumps({'username': 'user', 'password': 'password'}),
                #                            headers={'Content-Type': 'application/json'})
                # auth_token = json.loads(auth_request.data)['access_token']
                # header = {'Authorization': f'JWT {auth_token}'}

                response = client.get('/item/test', headers=self.header)

                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 999.99, 1).save_to_db()
                # UserModel('user', 'password').save_to_db()
                # auth_request = client.post('/auth',
                #                            data=json.dumps({'username': 'user', 'password': 'password'}),
                #                            headers={'Content-Type': 'application/json'})
                # auth_token = json.loads(auth_request.data)['access_token']
                # header = {'Authorization': f'JWT {auth_token}'}

                response = client.get('/item/testitem', headers=self.header)

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'testitem', 'price': 999.99}, json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 999.99, 1).save_to_db()

                response = client.delete('/item/testitem')

                self.assertEqual(200, response.status_code)
                self.assertEqual({'message': 'Item deleted'}, json.loads(response.data))



    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()

                response = client.post('/item/testitem', data={'price': 999.99, 'store_id': 1})

                self.assertEqual(201, response.status_code)

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 999.99, 1).save_to_db()

                response = client.post('/item/testitem', data={'price': 999.99, 'store_id': 1})

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "An item with name 'testitem' already exists."},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()

                response = client.put('/item/testitem', data={'price': 9.99, 'store_id': 1})

                self.assertEqual(200, response.status_code)
                self.assertEqual(9.99, ItemModel.find_by_name('testitem').price)
                self.assertDictEqual({'name': 'testitem', 'price': 9.99}, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 999.99, 1).save_to_db()

                response = client.put('/item/testitem', data={'price': 9.99, 'store_id': 1})

                self.assertEqual(9.99, ItemModel.find_by_name('testitem').price)
                self.assertDictEqual({'name': 'testitem', 'price': 9.99}, json.loads(response.data))

                self.assertEqual(200, response.status_code)

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 999.99, 1).save_to_db()
                ItemModel('testitem2', 99.99, 1).save_to_db()

                response = client.get('/items')
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'items': [{'name': 'testitem', 'price': 999.99},
                                      {'name': 'testitem2', 'price': 99.99}]}, json.loads(response.data))