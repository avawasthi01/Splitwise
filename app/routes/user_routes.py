from flask import jsonify, request, Blueprint
from app.models.user import User

# Create a blueprint
user_bp = Blueprint('users', __name__)


# Use the blueprint instance to define routes
@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    user = User(**data)
    user.save()
    return jsonify({"message": "User registered successfully"}), 201
