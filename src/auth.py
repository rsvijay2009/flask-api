from flask import Blueprint, request
from src.schema import UsersSchema
from src.users import Users
from src.database import db
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/")


@auth.post("login")
@swag_from('./docs/auth/login.yml')
def login():
    json_data = request.get_json()

    if not json_data:
        return {"message": "No input data provided"}, 400

    email = json_data['email']
    password = json_data['password']

    user = Users.query.filter_by(email=email).first()

    if user:
        is_password_correct = check_password_hash(user.password, password)

        if is_password_correct:
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                "data": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "mobile": user.mobile,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }

        return {"message": "Invalid password"}, 401

    return {"message": "Invalid login credentials"}, 401


@auth.post("register")
@swag_from('./docs/registration.yml')
def register():
    json_data = request.get_json()

    if not json_data or len(json_data) == 0:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        schema = UsersSchema()
        errors = schema.load(json_data)

        if not errors:
            return {"error": errors}
        else:
            first_name = json_data['first_name']
            last_name = json_data['last_name']
            email = json_data['email']
            password = json_data['password']
            mobile = json_data['mobile']

            password_hash = generate_password_hash(password)

            email_exists = Users.query.filter_by(email=email).first()

            if email_exists:
                return {"message": "Email already exists"}

            user = Users(first_name=first_name, last_name=last_name,
                         email=email, password=password_hash, mobile=mobile)
            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully!"}
    except ValidationError as err:
        return {"errors": err.messages}, 422
