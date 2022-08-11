from app.extensions import db


class Permission(db.Model):
    __tablename__ = "permissions"
    PERMISSIONS = {"can_create": "can_create", "can_delete": "can_delete", "can_update": "can_update",
                   "can_read": "can_read", "can_upgrade": "can_upgrade"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(*PERMISSIONS, name="permission_types"), nullable=False, unique=True)

    # Roles that are using this particular permission
    list_of_role_id = db.relationship("RoleHasPermissions", backref="permission_detail", cascade="delete")
    list_of_extra_permission = db.relationship("UserHasExtraPermission", backref="extra_permission_detail",
                                               cascade="delete")

    def save(self):
        db.session.add(self)
        db.session.commit()


class Role(db.Model):
    __tablename__ = "roles"
    ROLE = {"normal": "Normal", "admin": "Admin", "super_admin": "Super Admin"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(*ROLE, name='role_types'), nullable=False, server_default="normal")

    list_of_users = db.relationship("UserHasRoles", backref="role_detail", cascade="delete")
    list_of_permission_id = db.relationship("RoleHasPermissions", backref="permissions_detail", cascade="delete")

    def save(self):
        db.session.add(self)
        db.session.commit()


class UserHasRoles(db.Model):
    # A role and permission row should be unique.
    __tablename__ = "user_has_roles"

    user_id = db.Column(db.ForeignKey("users.id"), primary_key=True)
    role_id = db.Column(db.ForeignKey("roles.id"), primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()


class RoleHasPermissions(db.Model):
    # A role and permission row should be unique.
    __tablename__ = "role_has_permissions"

    permission_id = db.Column(db.ForeignKey("permissions.id"), primary_key=True)
    role_id = db.Column(db.ForeignKey("roles.id"), primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()


class UserHasExtraPermission(db.Model):
    # Extra permissions to a user irrespective of role
    __tablename__ = "user_has_extra_permissions"

    permission_id = db.Column(db.ForeignKey("permissions.id"), primary_key=True)
    user_id = db.Column(db.ForeignKey("users.id"), primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
