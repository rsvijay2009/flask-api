from crypt import methods
from flask import Blueprint, request, jsonify
import jwt
from src.database import Posts
from src.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

posts = Blueprint('post', __name__, url_prefix='/api/v1/posts/')


@posts.route('/', methods=['POST'])
@jwt_required()
def create_post():
    json_data = request.get_json()

    if not json_data or len(json_data) == 0:
        return {"message": "No input data provided"}, 400
    try:
        title = json_data['title']
        content = json_data['content']
        author_id = get_jwt_identity()

        post = Posts(title=title, content=content, author_id=author_id)
        db.session.add(post)
        db.session.commit()

        return {"message": "Post created successfully!"}
    except ValidationError as err:
        return {"errors": err.messages}, 422


@posts.route('/all', methods=['GET'])
def posts_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)
    posts = Posts.query.order_by(Posts.id.desc()).paginate(
        page=page, per_page=per_page)

    if len(posts.items):
        data = []
        for post in posts.items:
            created_at = post.created_at
            updated_at = post.updated_at
            published_at = post.published_at

            if created_at:
                created_at = created_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                created_at = ""

            if updated_at:
                updated_at = updated_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                updated_at = ""

            if published_at:
                published_at = published_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                published_at = ""

            data.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "author_id": post.author_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "published_at": published_at
            })
            base_url = request.base_url
            prev_url = ""
            next_url = ""

            if posts.prev_num:
                prev_url = base_url+"?page="+str(posts.prev_num)

            if posts.next_num:
                next_url = base_url+"?page="+str(posts.next_num)

            meta = {
                "page": posts.page,
                "pages": posts.pages,
                "total": posts.total,
                "prev": prev_url,
                "next": next_url,
                "has_prev": posts.has_prev,
                "has_next": posts.has_next
            }

        return jsonify({"data": data, "meta": meta}), 200
    else:
        return jsonify({"data": "No posts available at the moment"}), 404


@posts.route("/", methods=['GET'])
@jwt_required()
def get_user_post():
    author_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)
    posts = Posts.query.filter_by(author_id=author_id).order_by(Posts.id.desc()).paginate(
        page=page, per_page=per_page)

    if len(posts.items):
        data = []
        for post in posts.items:
            created_at = post.created_at
            updated_at = post.updated_at
            published_at = post.published_at

            if created_at:
                created_at = created_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                created_at = ""

            if updated_at:
                updated_at = updated_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                updated_at = ""

            if published_at:
                published_at = published_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                published_at = ""

            data.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "author_id": post.author_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "published_at": published_at
            })
            base_url = request.base_url
            prev_url = ""
            next_url = ""

            if posts.prev_num:
                prev_url = base_url+"?page="+str(posts.prev_num)

            if posts.next_num:
                next_url = base_url+"?page="+str(posts.next_num)

            meta = {
                "page": posts.page,
                "pages": posts.pages,
                "total": posts.total,
                "prev": prev_url,
                "next": next_url,
                "has_prev": posts.has_prev,
                "has_next": posts.has_next
            }

        return jsonify({"data": data, "meta": meta}), 200
    else:
        return jsonify({"data": "No posts available at the moment"}), 404


@posts.route("<int:id>", methods=['GET'])
@jwt_required()
def get_post(id):
    try:
        current_user = get_jwt_identity()
        post = Posts.query.filter_by(author_id=current_user, id=id).first()

        if not post:
            return {'message': 'Item not found'}, 404
        else:
            created_at = post.created_at
            updated_at = post.updated_at
            published_at = post.published_at

            if created_at:
                created_at = created_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                created_at = ""

            if updated_at:
                updated_at = updated_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                updated_at = ""

            if published_at:
                published_at = published_at.strftime("%Y/%m/%d, %H:%M:%S")
            else:
                published_at = ""

            return {
                "data": {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "published": post.published,
                    "author_id": post.author_id,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "published_at": published_at
                }
            }

    except ValidationError as err:
        return {"errors": err.messages}, 422


@posts.route("<int:id>", methods=['PUT'])
@jwt_required()
def update_post(id):
    json_data = request.get_json()

    if not json_data or len(json_data) == 0:
        return {"message": "No input data provided"}, 400

    try:
        title = json_data['title']
        content = json_data['content']
        current_user = get_jwt_identity()
        post = Posts.query.filter_by(author_id=current_user, id=id).first()

        if not post:
            return {'message': 'You are not authorized to edit this item'}, 404
        else:
            post.title = title
            post.content = content

            return {
                "data": {
                    "title": post.title,
                    "content": post.content,
                    "published": post.published,
                    "author_id": post.author_id,
                    "created_at": post.created_at,
                    "updated_at": post.updated_at,
                    "published_at": post.published_at
                }
            }

    except ValidationError as err:
        return {"errors": err.messages}, 422


@posts.route("<int:id>", methods=['DELETE'])
@jwt_required()
def delete_post(id):
    try:
        current_user = get_jwt_identity()
        post = Posts.query.filter_by(author_id=current_user, id=id).first()

        if not post:
            return {'message': 'You are not authorized to delete this item'}, 404

        db.session.delete(post)
        db.session.commit()

        return {'msg': 'Post deleted successfully!'}
    except ValidationError as err:
        return {"errors": err.messages}, 422
