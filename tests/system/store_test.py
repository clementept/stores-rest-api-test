import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/teststore')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('teststore'))
                self.assertDictEqual({'name': 'teststore', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore')

                self.assertIsNotNone(StoreModel.find_by_name('teststore'))

                response = client.post('/store/teststore')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'teststore' already exists."},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore')

                response = client.delete('/store/teststore')

                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('teststore'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore')

                response = client.get('/store/teststore')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'teststore', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/teststore')

                response = client.get('/store/nostore')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 999.99, 1).save_to_db()

                response = client.get('/store/teststore')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'teststore', 'items': [{'name': 'testitem', 'price': 999.99}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()

                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'teststore', 'items': []}]}, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('teststore').save_to_db()
                ItemModel('testitem', 999.99, 1).save_to_db()

                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'teststore', 'items': [{'name': 'testitem', 'price': 999.99}]}]}, json.loads(response.data))