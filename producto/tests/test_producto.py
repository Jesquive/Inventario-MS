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
            db.session.close()
            db.drop_all()
            db.create_all()
  
    def register_user(self, email='user@test.com', password='test1234'):
        user_data = {
                'email': email,
                'password': password
                }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email='user@test.com', password='test1234'):
        user_data = {
                'email': email,
                'password': password
                }
        return self.client().post('/auth/login', data = user_data)

    def test_producto_creation(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        res = self.client().post(
                '/productos/',
                headers=dict(Authorization='Bearer '+ access_token),
                data = self.producto
                )
        self.assertEqual(res.status_code, 201)
        self.assertIn('ASUS', str(res.data))

    def test_api_can_get_all_productos(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        res = self.client().post(
                '/productos/',
                headers = dict(Authorization='Bearer ' + access_token),
                data = self.producto
                )
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
                '/productos/',
                headers=dict(Authorization='Bearer ' + access_token)
                )

        self.assertEqual(res.status_code, 200)
        self.assertIn('ASUS', str(res.data))
    
    def test_api_can_get_producto_by_id(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        rv = self.client().post(
                '/productos/',
                headers = dict(Authorization='Bearer ' + access_token),
                data = self.producto
                )
        self.assertEqual(rv.status_code, 201)

        result_in_json = json.loads(rv.data.decode())
        result = self.client().get(
                '/productos/{}'.format(result_in_json['id']),
                headers=dict(Authorization='Bearer ' + access_token)
                )

        self.assertEqual(result.status_code, 200)
        self.assertIn('ASUS', str(result.data))

    def test_producto_can_be_edited(self):
        self.register_user()
        result = self.login_user()
        access_token = str(json.loads(result.data.decode())['access_token'])

        rv = self.client().post(
                '/productos/',
                headers=dict(Authorization='Bearer ' + access_token),
                data={'name': 'ASUS-RTX2080'}
                )
        
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())

        rv = self.client().put(
                '/productos/{}'.format(results['id']),
                headers=dict(Authorization='Bearer ' + access_token),
                data = {
                    'name': 'ASUS-RTX2080TI'
        })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get(
                '/productos/{}'.format(results['id']),
                headers=dict(Authorization='Bearer ' + access_token)
                )
        self.assertIn('ASUS-RTX', str(results.data))

    def test_producto_delete(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
                '/productos/',
                headers = dict(Authorization='Bearer '+ access_token),
                data={'name': 'ASUS-GTX1050' })

        self.assertEqual(rv.status_code, 201)

        results = json.loads(rv.data.decode())
        res = self.client().delete(
                '/productos/{}'.format(results['id']),
                headers=dict(Authorization='Bearer ' + access_token)
                )

        self.assertEqual(res.status_code, 200)
        result = self.client().get(
                '/productos/1',
                headers=dict(Authorization='Bearer ' + access_token)
                )
        self.assertEqual(result.status_code, 404)
    


if __name__ == "__main__":
     unittest.main()


