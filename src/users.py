from flask import Blueprint, jsonify, request
from src.database import Users
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

users = Blueprint('users', __name__, url_prefix='/api/v1/user/')


@users.get('list')
@swag_from('./docs/user_list.yml')
def user_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)

    users = Users.query.order_by(Users.id.desc()).paginate(
        page=page, per_page=per_page)

    if len(users.items):
        data = []

        for user in users.items:
            created_at = user.created_at
            updated_at = user.updated_at

            if created_at:
                created_at = created_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                created_at = ""

            if updated_at:
                updated_at = updated_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                updated_at = ""

            data.append({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "mobile": user.mobile,
                "created_at": created_at,
                "updated_at": updated_at
            })
            base_url = request.base_url
            prev_url = ""
            next_url = ""

            if users.prev_num:
                prev_url = base_url+"?page="+str(users.prev_num)

            if users.next_num:
                next_url = base_url+"?page="+str(users.next_num)
            meta = {
                "page": users.page,
                "pages": users.pages,
                "total": users.total,
                "prev": prev_url,
                "next": next_url,
                "has_prev": users.has_prev,
                "has_next": users.has_next
            }

        return jsonify({"data": data, "meta": meta}), 200
    else:
        return jsonify({"data": "No users available at the moment"}), 404


@users.get('profile')
@jwt_required()
@swag_from('./docs/user_profile.yml')
def profile():
    user_id = get_jwt_identity()
    user = Users.query.filter_by(id=user_id).first()

    if(user):
        return jsonify({
            "data": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "mobile": user.mobile,
                "created_at": user.created_at.strftime("%Y/%m/%d, %H:%M:%S")
            }
        }), 200
    else:
        return jsonify({"data": "User not found"}), 404
