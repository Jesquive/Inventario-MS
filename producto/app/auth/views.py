from . import auth_blueprint
from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify, current_app
from app.models import User

class RegistrationView(MethodView):

    def post(self):
        user = User.query.filter_by(email=request.form['email']).first()
        if not user:
            try:
                post_data = request.form
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                user.save()
                response = {
                        'message': 'You registered successfully.'
                        }
                return make_response(jsonify(response)), 201

            except Exception as e:
                
                response = {
                        'message': str(e)
                        }
                return make_response(jsonify(response)), 401
        else:
            response = {
                    'message': 'User already exists. Please login.'
                    }
            return make_response(jsonify(response)), 202
class LoginView(MethodView):
    def post(self):
        try:
            user = User.query.filter_by(email=request.form['email']).first()

            if user and user.password_is_valid(request.form['password']):
                access_token = str(user.generate_token(user.id))
                
                if access_token:
                    response = {
                            'message': 'You logged in successfully.',
                            'access_token': access_token
                            }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                        'message': 'Invalid email or password'
                        }
                return make_response(jsonify(response)), 401
        except Exception as e:
            response = {
                    'message': str(e)
                    }
            return make_response(jsonify(response)), 500
class LogoutView(MethodView):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_token(auth_token)
            if not isinstance(resp, str):
                try:
                    responseObject = {
                            'status': 'success',
                            'message': 'Successfully logged out'
                            }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    response = {
                            'status': 'Logout fail',
                            'message': e
                            }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                        'status': 'logout fail',
                        'message': resp
                        }
                return make_response(jsonify(response)), 401
        else:
            res = {
                    'status': 'logout fail',
                    'message': 'Provide a valid auth token'
                    }
            return make_response(jsonify(res)), 403

registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')

auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods = ['POST'])
auth_blueprint.add_url_rule('/auth/logout', view_func=logout_view, methods = ['POST'])
