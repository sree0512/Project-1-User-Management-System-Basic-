from flask import Blueprint, request, jsonify
from app.services.user import get_user_by_id, update_user, change_password, delete_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.user_schemas import UpdateUserRequest, ChangePasswordRequest, RegisterRequest
from pydantic import ValidationError


# Create Blueprint for user-related routes
user_bp = Blueprint("user", __name__)

# For now, hardcoded user ID; later, replace with JWT extraction
# current_user_id = 1


# -----------------------------
# GET /user/profile
# Fetch current user info
# -----------------------------
@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        print("Request reached /profile")  # confirm route is hit
        user_id = get_jwt_identity()
        print("JWT Identity:", user_id)  # debug
        user = get_user_by_id(user_id)
        print("Fetched user:", user) #debug
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user), 200
    except Exception as e:
        print("ERROR:", e)  # full traceback
        return jsonify({"error": "Internal server error"}), 500

# -----------------------------
# PUT /user/update
# Update user's full_name and/or email
# -----------------------------
@user_bp.route("/update", methods=["PUT"])
@jwt_required()
def update():
    try:
        # Get the current user id from JWT
        user_id = get_jwt_identity()

        # Fetch JSON input
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON data"}), 400

        # Validate input using Pydantic
        try:
            req = UpdateUserRequest(**data)
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400

        # Prepare fields to update (only non-null fields)
        updates = {}
        if req.username:
            updates["username"] = req.username
        if req.email:
            updates["email"] = req.email

        if not updates:
            return jsonify({"error": "No valid fields to update"}), 400

        # Call service layer to update the user
        updated_user = update_user(user_id=user_id, **updates)

        # Return updated user info
        return jsonify(updated_user), 200

    except ValueError as ve:
        # e.g., duplicate email
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # Catch-all for unexpected errors
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500  
# -----------------------------
# PUT /user/change-password
# Change the user's password
# -----------------------------
@user_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password_route():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON data"}), 400
        try:
            req = ChangePasswordRequest(**data)
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400

        old_password = req.old_password
        new_password = req.new_password

        # Call service layer to change password
        change_password(user_id, old_password, new_password)
        return jsonify({"message": "Password changed successfully"}), 200

    except ValueError as ve:  # e.g., user not found
        return jsonify({"error": str(ve)}), 404
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

# -----------------------------
# DELETE /user/delete
# Delete the current user
# -----------------------------
@user_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user_route():
    try:
        user_id = get_jwt_identity()
        # For the current user, no JSON input is needed
        delete_user(user_id)
        return jsonify({"message": "Deleted user successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
