from app.extensions import db
from app import create_app
from app.blueprints.user.models import User
from app.blueprints.roles.models import Permission, Role, RoleHasPermissions, UserHasRoles

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # create four permissions
    Permission(name="can_read").save()
    Permission(name="can_create").save()
    Permission(name="can_update").save()
    Permission(name="can_delete").save()
    Permission(name="can_upgrade").save()

    # create three roles
    Role(name="normal").save()
    Role(name="admin").save()
    Role(name="super_admin").save()

    # Associate Permissions to those Roles
    RoleHasPermissions(permission_id=1, role_id=1).save()

    RoleHasPermissions(permission_id=1, role_id=2).save()
    RoleHasPermissions(permission_id=2, role_id=2).save()
    RoleHasPermissions(permission_id=3, role_id=2).save()
    RoleHasPermissions(permission_id=4, role_id=2).save()

    RoleHasPermissions(permission_id=1, role_id=3).save()
    RoleHasPermissions(permission_id=2, role_id=3).save()
    RoleHasPermissions(permission_id=3, role_id=3).save()
    RoleHasPermissions(permission_id=4, role_id=3).save()
    RoleHasPermissions(permission_id=5, role_id=3).save()

    # create three users
    User(username="normal", email="normaluser@gmail.com", password="normal").save()
    User(username="admin", email="adminuser@gmail.com", password="admin").save()
    User(username="superadmin", email="superadmin@gmail.com", password="superadmin").save()

    # Associate roles with all 3 users
    UserHasRoles(user_id=1, role_id=1).save()
    UserHasRoles(user_id=2, role_id=2).save()
    UserHasRoles(user_id=3, role_id=3).save()
