from flask import Blueprint
from app.blueprints.roles.models import Permission

roles = Blueprint("roles", __name__)
