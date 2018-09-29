import unittest
import os
import json
from app import create_app, db

class ProductoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.producto = {'name': 'ASUS-GTX1080'}
        
        with self.app.app_context():
            db.create_all()

    def test_producto_creation(self):
        res = self.client().post('/productos/', data = self.producto)
        self.assertEqual(res.status_code, 201)
        self.assertIn('ASUS', str(res.data))

    def test_api_can_get_all_productos(self):
        res = self.client().post('/productos/', data = self.producto)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/productos/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('ASUS', str(res.data))
    
    def test_api_can_get_producto_by_id(self):
        rv = self.client().post('/productos/', data = self.producto)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
                '/productos/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('ASUS', str(result.data))

    def test_producto_can_be_edited(self):
        rv = self.client().post(
                '/productos/',
                data={'name': 'ASUS-RTX2080'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
                '/productos/1',
                data = {
                    'name': 'ASUS-RTX2080TI'
        })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/productos/1')
        self.assertIn('ASUS-RTX', str(results.data))

    def test_producto_delete(self):
        rv = self.client().post(
                '/productos/',
                data={'name': 'ASUS-GTX1050' })
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/productos/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/productos/1')
        self.assertEqual(result.status_code, 404)
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
     unittest.main()


