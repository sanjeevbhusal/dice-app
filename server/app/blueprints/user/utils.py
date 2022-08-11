from datetime import datetime, timedelta
from flask import current_app, request
from jwt.exceptions import InvalidTokenError
from functools import wraps

from app.blueprints.roles.models import UserHasRoles, Role, Permission, UserHasExtraPermission
from app.blueprints.user.exceptions import UnknownUserException, NoAccessTokenException, NotAuthorizedException

from app.blueprints.user.models import User
import jwt


def create_token(user_id):
    return jwt.encode({"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=24)},
                      current_app.config["SECRET_KEY"])


def decode_token(token):
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms="HS256")
    except InvalidTokenError as err:
        raise err


def login_required(f):
    def decorator(*args, **kwargs):
        try:
            access_token = request.headers.get("access_token")
            if not access_token:
                raise NoAccessTokenException
            token = decode_token(access_token)
            user = User.query.get(token.get("user_id"))
            if not user:
                raise UnknownUserException
            return f(user, *args, **kwargs)
        except NoAccessTokenException as err:
            return {"error": err.message}, 400
        except InvalidTokenError as err:
            return {"error": "Token is invalid"}, 400
        except UnknownUserException as err:
            return {'error': err.message}, 404

    return decorator


def admin_required(f):
    def decorator(*args, **kwargs):
        try:
            access_token = request.headers.get("access_token")
            if not access_token:
                raise NoAccessTokenException
            token = decode_token(access_token)
            user = User.query.get(token.get("user_id"))
            if not user:
                raise UnknownUserException
            user_role = user.role
            if user_role == "normal":
                raise NotAuthorizedException
            return f(*args, **kwargs)
        except NoAccessTokenException as err:
            return {"error": err.message}, 400
        except InvalidTokenError as err:
            return {"error": "Token is invalid"}, 400
        except UnknownUserException as err:
            return {'error': err.message}, 404
        except NotAuthorizedException as err:
            return {"error": err.message}, 403

    return decorator


def assign_role_to_user(user_id, role):
    role = Role.query.filter_by(name=role)
    UserHasRoles(user_id=user_id, role_id=role.id).save()


def assign_permission_to_user(user_id, permission):
    permission = Permission.query.filter_by(name=permission)
    UserHasExtraPermission(user_id=user_id, permission_id=permission.id).save()


def upgrade_permission_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            access_token = request.headers.get("access_token")
            if not access_token:
                raise NoAccessTokenException
            token = decode_token(access_token)
            user = User.query.get(token.get("user_id"))
            if not user:
                raise UnknownUserException
            list_of_allowed_permissions = get_list_of_allowed_permission(token.get("user_id"))
            if "can_upgrade" not in list_of_allowed_permissions:
                raise NotAuthorizedException
            return f(*args, **kwargs)
        except NoAccessTokenException as err:
            return {"error": err.message}, 400
        except InvalidTokenError as err:
            return {"error": "Token is invalid"}, 400
        except UnknownUserException as err:
            return {'error': err.message}, 404
        except NotAuthorizedException as err:
            return {"error": err.message}, 403

    return decorator


def get_list_of_allowed_permission(user_id):
    user = User.query.get(user_id)
    list_of_roles_id = user.list_of_role_id
    list_of_role = [role_id.role_detail for role_id in list_of_roles_id]
    list_of_permission_id = [permission_id for role in list_of_role for permission_id in role.list_of_permission_id]
    list_of_permissions = [permission_id.permission_detail for permission_id in list_of_permission_id]

    return list_of_permissions
