from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config
from flask import request, jsonify, abort, make_response
#Initialize sql-alchemy

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Producto, User
    
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    @app.route('/productos/', methods = ['POST', 'GET'])
    def productos():
        auth_header = str(request.headers.get('Authorization'))
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            
            if not isinstance(user_id, str):

                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        producto = Producto(name=name, created_by=user_id)
                        producto.save()
                        response = jsonify({
                            'id': producto.id,
                            'name': producto.name,
                            'date_created': producto.date_created,
                            'date_modified': producto.date_modified,
                            'created_by': user_id
                        })
                        return make_response(response), 201
                
                
                else:
                    productos = Producto.query.filter_by(created_by=user_id)
                    results = []

                    for producto in productos:
                        obj = {
                            'id': producto.id,
                            'name': producto.name,
                            'date_created': producto.date_created,
                            'date_modified': producto.date_modified,
                            'created_by': producto.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            
            else:
                message = user_id
                response = {
                        'message': message
                        }
                return make_response(jsonify(response)), 401
            

    @app.route('/productos/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
    def producto_manipulation(id, **kwargs):
        auth_header =str(request.headers.get('Authorization'))
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            
            if not isinstance(user_id, str):

                producto = Producto.query.filter_by(id = id).first()
                if not producto:
                    abort(404)
                if request.method == 'DELETE':
                    producto.delete()
                    return {
                        "message": "producto {} eliminado correctamente".format(producto.id)}, 200
                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    producto.name = name
                    producto.save()
                    response = {
                        'id': producto.id,
                        'name': producto.name,
                        'date_created': producto.date_created,
                        'date_modified': producto.date_modified,
                        'created_by': producto.created_by
                    }
            
                    return make_response(jsonify(response)), 200
                else:
                    response = jsonify({
                        'id': producto.id,
                        'name': producto.name,
                        'date_created': producto.date_created,
                        'date_modified': producto.date_modified,
                        'created_by': producto.created_by
                    })
            
                    return make_response(response), 200
            else:
                print(user_id)
                message = user_id
                response = {
                        'message': message
                        }
                return make_response(jsonify(response)), 401

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app
