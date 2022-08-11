from flask import Blueprint, request
from jwt import InvalidTokenError

from app.blueprints.user.models import User
from app.blueprints.user.schema import UserResponseSchema, UserRegisterSchema, UserUpdateSchema, UserLoginSchema, \
    UserUpgradeSchema, AssignRoleSchema, AssignPermissionSchema
from app.blueprints.user.exceptions import EmailAlreadyExistException, \
    PasswordDoesnotMatchException, UnknownEmailException, UnknownUserException, NoAccessTokenException
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from app.blueprints.user.utils import create_token, decode_token, \
    get_list_of_allowed_permission, upgrade_permission_required, assign_role_to_user, \
    assign_permission_to_user

user = Blueprint("users", __name__)


@user.route("/register", methods=["POST"])
def register():
    try:
        result = UserRegisterSchema().load(request.form)
        existing_user = User.get_by_email(result["email"])
        if existing_user:
            raise EmailAlreadyExistException
        User(**result).save()
        return {"message": "User registered Successfully"}, 201
    except BadRequest as err:
        return {"message": err.description}, 400
    except ValidationError as err:
        return {"message": err.messages}
    except EmailAlreadyExistException as err:
        return {"error": {"email_error": err.message}}


@user.route("/login", methods=["POST"])
def login_user():
    try:
        result = UserLoginSchema().load(request.form)
        existing_user = User.get_by_email(result["email"])
        if not existing_user:
            raise UnknownEmailException
        if not existing_user.authenticate(result["password"]):
            raise PasswordDoesnotMatchException()
        return {"user": {"token": create_token(existing_user.id), **UserResponseSchema().dump(existing_user)}}, 200
    except BadRequest as err:
        return {"error": err.description}, 400
    except ValidationError as err:
        return {"error": err.messages}, 400
    except UnknownEmailException as err:
        return {"error": {"email_error": err.message}}, 404
    except PasswordDoesnotMatchException as err:
        return {"error": {"password_error": err.message}}, 403


@user.route("/users")
def get_all_users():
    user_list = User.query.order_by(User.id).all()
    return {"users": UserResponseSchema(many=True).dump(user_list)}


@user.route("/users/<int:user_id>")
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            raise UnknownUserException
        return {"user": UserResponseSchema().dump(user)}
    except UnknownUserException as err:
        return {"error": err.message}, 404


@user.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        result = UserUpdateSchema().load(request.form)
        user = User.query.get(user_id)
        if not user:
            raise UnknownUserException
        user.update(result)
        return {"message": "Credentials has been updated successfully"}, 200
    except BadRequest as err:
        return {"error": err.description}, 400
    except ValidationError as err:
        return {"error": err.messages}, 400
    except UnknownUserException as err:
        return {"error": err.message}, 404


@user.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            raise UnknownUserException
        user.delete()
        return {"message": "User has been deleted successfully"}, 200
    except ValidationError as err:
        return {"error": err.messages}, 400
    except UnknownUserException as err:
        return {"error": err.message}, 404


@user.route("/users/assign_role/<int:user_id>", methods=["PUT"])
@upgrade_permission_required
def assign_role(user_id):
    try:
        role_to_assign = AssignRoleSchema().load(request.form)
        user = User.query.get(user_id)
        if not user:
            raise UnknownUserException
        assign_role_to_user(role_to_assign)
        return {"message": "User has been upgraded"}, 200
    except BadRequest as err:
        return {"error": err.description}
    except ValidationError as err:
        return {"error": err.messages}, 400
    except UnknownUserException as err:
        return {"error": err.message}, 404


@user.route("/users/assign_permission/<int:user_id>", methods=["PUT"])
@upgrade_permission_required
def assign_permission(user_id):
    try:
        permission_to_assign = AssignPermissionSchema().load(request.form)
        user = User.query.get(user_id)
        if not user:
            raise UnknownUserException
        assign_permission_to_user(permission_to_assign)
        return {"message": "User has been upgraded"}, 200
    except BadRequest as err:
        return {"error": err.description}
    except ValidationError as err:
        return {"error": err.messages}, 400
    except UnknownUserException as err:
        return {"error": err.message}, 404


@user.route("/users/validate_token")
def validate_token():
    try:
        token = request.headers.get("access_token")
        if not token:
            raise NoAccessTokenException
        decode_token(token)
        return {"validated": True}
    except NoAccessTokenException as err:
        return {"error": err.message, "validated": False}
    except InvalidTokenError as err:
        return {"error": "Token is invalid", "validated": False}, 400
