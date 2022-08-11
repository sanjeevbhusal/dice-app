from flask import Blueprint, request, jsonify
from app.blueprints.posts.models import Post
from app.blueprints.posts.schema import PostRegisterSchema, PostResponseSchema, PostUpdateSchema
from app.blueprints.posts.exceptions import PostNotFoundException
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

post = Blueprint("posts", __name__, url_prefix="/posts")


@post.route("/")
def get_all_posts():
    post_list = Post.query.all()
    return jsonify(PostResponseSchema(many=True).dump(post_list)), 200


@post.route("/<int:post_id>")
def get_post_by_id(post_id):
    try:
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException
        return {"post": {"title": "Hello Post"}}
        return {"post": PostResponseSchema().dump(post)}
    except PostNotFoundException as err:
        return {"error": err.message}, 404


@post.route("/", methods=["POST"])
def create_post():
    try:
        result = PostRegisterSchema().load(request.form)
        Post(**result).save()
        return {"message": "Successfully created a Post"}, 201
    except BadRequest as err:
        return {"error": err.description}, 400
    except ValidationError as err:
        return {"error": err.messages}, 400


@post.route("/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    try:
        result = PostUpdateSchema().load(request.form)
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException
        post.update(result)
        return {"message": "Post has been updated successfully"}, 200
    except ValidationError as err:
        return {"error": err.messages}, 400
    except PostNotFoundException as err:
        return {"error": err.message}, 400
    except BadRequest as err:
        return {"error": err.description}, 400


@post.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    try:
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException
        post.delete()
        return {"message": "Post has been deleted successfully."}
    except PostNotFoundException as err:
        return {"error": err.message}, 404
