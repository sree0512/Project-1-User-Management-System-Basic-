
from flask import Blueprint, request, jsonify
from app.services.auth import create_user, get_user_by_email, verify_password
import psycopg2
from flask_jwt_extended import create_access_token
from app.schemas.user_schemas import RegisterRequest, LoginRequest
from pydantic import ValidationError

#creating blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON data"}), 400
        try:
            req = RegisterRequest(**data)
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400

        username = req.username
        email = req.email
        password = req.password
        
        user = create_user(username=username, email=email, password=password)
        return jsonify({"user":user}), 201
        
    except ValueError as ve:
        # Handle duplicate email gracefully
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # Catch other DB errors
        return jsonify({"error":str(e)}), 500
    

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON data"}), 400
        try:
            req = LoginRequest(**data)
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400
        
        email= req.email
        password = req.password
        
        user = get_user_by_email(email)
        if not user or not verify_password(password, user['password_hash']):
            return jsonify({"error": "Invalid credentials"}), 401
        # generate JWT token
        access_token = create_access_token(identity=str(user['id']))
        return jsonify({"access_token": access_token}), 200
        # return jsonify({"message": "Login Succesfully"}), 200 
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500
    
    