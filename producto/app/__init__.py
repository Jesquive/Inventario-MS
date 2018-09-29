from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config
from flask import request, jsonify, abort
#Initialize sql-alchemy

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Producto
    
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    @app.route('/productos/', methods = ['POST', 'GET'])
    def productos():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                producto = Producto(name=name)
                producto.save()
                response = jsonify({
                    'id': producto.id,
                    'name': producto.name,
                    'date_created': producto.date_created,
                    'date_modified': producto.date_modified
                    })
                response.status_code = 201
                return response
        else:
            productos = Producto.get_all()
            results = []

            for producto in productos:
                obj = {
                        'id': producto.id,
                        'name': producto.name,
                        'date_created': producto.date_created,
                        'date_modified': producto.date_modified
                    }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/productos/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
    def producto_manipulation(id, **kwargs):
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
            response = jsonify({
                'id': producto.id,
                'name': producto.name,
                'date_created': producto.date_created,
                'date_modified': producto.date_modified
                })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'id': producto.id,
                'name': producto.name,
                'date_created': producto.date_created,
                'date_modified': producto.date_modified
                })
            response.status_code = 200
            return response

    return app
