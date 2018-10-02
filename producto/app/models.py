from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    productos = db.relationship(
            'Producto', order_by='Producto.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
    def generate_token(self, user_id):
        try:
            payload = {
                    'exp': datetime.utcnow() + timedelta(minutes=1440),
                    'iat': datetime.utcnow(),
                    'sub': user_id
                    }
            jwt_string = jwt.encode(
                    payload,
                    current_app.config.get('SECRET'),
                    algorithm='HS256'
                    )
            
            return jwt_string.decode('utf-8')
        except Exception as e:
            return str(e)
    @staticmethod
    def decode_token(token):
        
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'), algorithm='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired token, Please login again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please register or login'


class Producto(db.Model):
    __tablename__= 'productos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
            db.DateTime, default=db.func.current_timestamp(),
            onupdate = db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))


    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod

    def get_all(user_id):
        return Producto.query.filter_by(created_by=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return ("<Producto: {}>".format(self.name))
