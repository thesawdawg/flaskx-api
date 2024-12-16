import importlib
import os
import sys
from pathlib import Path

from flask_restx import Api, Resource, fields
from app.models import User as UserModel


def register_routes(api: Api):
    """
    Dynamically register routes from a specified directory.
    
    :param api: Flask-RESTX API instance
    """
    # Namespace for user-related routes
    user_ns = api.namespace('users', description='User operations')
    
    # User model for request/response
    user_model = api.model('User', {
        'id': fields.Integer(readonly=True, description='User unique identifier'),
        'username': fields.String(required=True, description='Username'),
        'email': fields.String(required=True, description='User email')
    })
    
    @user_ns.route('/')
    class UserList(Resource):
        @user_ns.doc('list_users')
        @user_ns.marshal_list_with(user_model)
        def get(self):
            """List all users"""
            users = UserModel.query.all()
            return [user.to_dict() for user in users]
        
        @user_ns.doc('create_user')
        @user_ns.param('username', 'Username')
        @user_ns.param('email', 'User email')
        @user_ns.param('password', 'User password')
        @user_ns.expect(api.model('UserCreate', {
            'username': fields.String(required=True, description='Username'),
            'email': fields.String(required=True, description='User email'),
            'password': fields.String(required=True, description='User password')
        }))
        @user_ns.marshal_list_with(user_model, code=201)
        def post(self):
            """Create a new user"""          
            data = api.payload

            new_user = UserModel(
                username=data['username'], 
                email=data['email']
            )
            new_user.set_password(data['password'])
            new_user.save()
            return new_user.to_dict(), 201
    
    @user_ns.route('/<int:user_id>')
    @user_ns.param('user_id', 'The user identifier')
    @user_ns.response(404, 'User not found')
    class User(Resource):
        @user_ns.doc('get_user')
        @user_ns.marshal_with(user_model)
        def get(self, user_id):
            """Fetch a user by ID"""
            user = UserModel.get_by_id(user_id)
            if not user:
                api.abort(404, f"User {user_id} not found")
            return user.to_dict()
        
        @user_ns.doc('delete_user')
        @user_ns.response(204, 'User deleted')
        def delete(self, user_id):
            """Delete a user"""            
            user = UserModel.get_by_id(user_id)
            if not user:
                api.abort(404, f"User {user_id} not found")
            
            user.delete()
            return '', 204
