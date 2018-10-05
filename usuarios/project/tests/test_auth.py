import unittest
import json
import time
from flask import Flask, current_app
from project.server import db
from project.server.models import User, BlacklistToken
from project.tests.base import BaseTestCase
class TestAuthBlueprint(BaseTestCase):


    def register_user(self, email, password):
        return self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email=email,
                    password=password
                    )),
                content_type='application/json'
                )
    
    def login_user(self, email, password):
        return self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=email,
                    password=password
                    )),
                content_type='application/json'
                )

    def status_user(self, resp):
        return self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer '+ json.loads(resp.data.decode())['auth_token']
                    )
                )

    def logout_user(self, resp):
        return self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(resp.data.decode())['auth_token']
                    )
                )

    def test_registration(self):
        with self.client:
            response = self.register_user('joe@gmail.com', '123456')

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.status_code, 201)
    def test_registered_with_already_registered_user(self):
        user = User(
                email='joe@gmail.com',
                password='test'
                )
        db.session.add(user)
        db.session.commit()
        with self.client:
            res = self.register_user('joe@gmail.com', '123456')
            data = json.loads(res.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                    data['message'] == 'User already exists. Please log in.')
            self.assertTrue(res.content_type == 'application/json')

            self.assertEqual(res.status_code, 202)
    
    def test_registered_user_login(self):
        with self.client:
            res = self.register_user('joe@gmail.com', '123456')
            data = json.loads(res.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                    data['message'] == 'Successfully registered.'
                    )
            self.assertTrue(data['auth_token'])
            self.assertTrue(res.content_type == 'application/json')
            self.assertEqual(res.status_code, 201)

            res = self.login_user('joe@gmail.com', '123456')
            data = json.loads(res.data.decode())
            
            self.assertTrue(data['status']=='success')
            self.assertTrue(data['message']=='Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(res.content_type == 'application/json')
            self.assertEqual(res.status_code, 200)

    def test_non_registered_user_login(self):
        with self.client:
            res = self.login_user('joe1@gmail.com', '123456')
            data = json.loads(res.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(res.content_type=='application/json')
            self.assertEqual(res.status_code, 404)

    def test_user_status(self):
        with self.client:
            res = self.register_user('joe@gmail.com', '123456')
            res2 = self.status_user(res)
            data = json.loads(res2.data.decode())
            
            self.assertTrue(data['status']=='success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'joe@gmail.com')
            self.assertTrue(data['data']['admin'] is 'true' or 'false')
            self.assertEqual(res2.status_code, 200)

    
    def test_valid_logout(self):
        with self.client:
            res = self.register_user('joe@gmail.com', '123456')
            data = json.loads(res.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                    data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(res.content_type=='application/json')
            self.assertEqual(res.status_code, 201)

            res = self.login_user('joe@gmail.com','123456')
            data = json.loads(res.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(res.content_type=='application/json')
            self.assertEqual(res.status_code, 200)

            resp = self.logout_user(res)
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(resp.status_code, 200)
    

    def test_invalid_logout(self):
        with self.client:
            res = self.register_user('joe@gmail.com', '123456')
            data = json.loads(res.data.decode())
            self.assertTrue(data['status']=='success')
            self.assertTrue(data['message']=='Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(res.content_type=='application/json')
            self.assertEqual(res.status_code, 201)

            resp = self.login_user('joe@gmail.com', '123456')
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message']=='Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(resp.content_type=='application/json')
            self.assertEqual(resp.status_code, 200)

            time.sleep(6)
            resp2 = self.logout_user(resp)
            data2 = json.loads(resp2.data.decode())
            self.assertTrue(data2['status']=='fail') 
            self.assertTrue(data2['message']=='Token blacklisted. Please log in again.')
            self.assertEqual(resp2.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        with self.client:
            res = self.register_user('joe@gmail.com', '123456')
            data = json.loads(res.data.decode())
            self.assertTrue(data['status']=='success')
            self.assertTrue(data['message']=='Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(res.content_type=='application/json')
            self.assertEqual(res.status_code, 201)

            resp = self.login_user('joe@gmail.com', '123456')
            data2 = json.loads(resp.data.decode())
            self.assertTrue(data2['status']=='success')
            self.assertTrue(data2['message']=='Successfully logged in.')
            self.assertTrue(data2['auth_token'])
            self.assertTrue(resp.content_type=='application/json')
            self.assertEqual(resp.status_code, 200)
            blacklist_token = BlacklistToken(
                    token=json.loads(resp.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()

            res= self.logout_user(resp)
            data= json.loads(res.data.decode())
            self.assertTrue(data['status']=='fail')
            
            self.assertTrue(data['message']=='Token blacklisted. Please log in again.')
            self.assertEqual(res.status_code, 401)
    def test_decode_auth_token(self):
            user= User(
               email='test@test.com',
               password='test'
               )
            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token(user.id)
            self.assertTrue(isinstance(auth_token, bytes))
            self.assertTrue(User.decode_auth_token(auth_token.decode('utf-8')==1))
    def test_valid_blacklisted_token_user(self):
        with self.client:
            res = self.register_user('joe@gmail.com', '123456')
            blacklist_token = BlacklistToken(token=json.loads(res.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            res2 = self.status_user(res)
            data= json.loads(res2.data.decode())
            self.assertTrue(data['status']=='fail')
            self.assertTrue(data['message']=='Token blacklisted. Please log in again.')
            self.assertEqual(res2.status_code, 401)
                    
    def test_user_status_malformed_bearer_token(self):
        with self.client:
            res = self.register_user('joe@gmail.com', '123456')

            res2 = self.client.get(
                    '/auth/status',
                    headers=dict(
                        Authorization='Bearer'+ json.loads(res.data.decode())['auth_token'])
                    )
            data=json.loads(res2.data.decode())
            
            self.assertTrue(data['status']=='fail')
            self.assertTrue(data['message']=='Bearer token malformed.')
            self.assertEqual(res2.status_code, 401)


if __name__ == '__main__':
    unittest.main()
