from marshmallow import fields, Schema, validates_schema
from marshmallow.exceptions import ValidationError


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserUpgradeSchema(Schema):
    make_admin = fields.Boolean()
    can_read = fields.Boolean()
    can_create = fields.Boolean()
    can_update = fields.Boolean()
    can_delete = fields.Boolean()


class AssignRoleSchema(Schema):
    role = fields.String(required=True)

    @validates_schema
    def validate_role(self, data, **kwargs):
        options = ["normal", "admin", "super_admin"]
        if data["role"] not in options:
            raise ValidationError("Role is not recognized.")


class AssignPermissionSchema(Schema):
    permission = fields.String(required=True)

    @validates_schema
    def validate_role(self, data, **kwargs):
        options = ["can_read", "can_write", "can_delete", "can_upgrade", "can_update"]
        if data["role"] not in options:
            raise ValidationError("Permission is not recognized.")


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserUpdateSchema(Schema):
    username = fields.String()
    password = fields.String()


class UserResponseSchema(Schema):
    id = fields.Integer(required=True)
    username = fields.String()
    email = fields.Email(required=True)
    role = fields.String(required=True)
    active = fields.Boolean(required=True)
    can_create = fields.Boolean()
    can_update = fields.Boolean()
    can_delete = fields.Boolean()
    can_read = fields.Boolean()
