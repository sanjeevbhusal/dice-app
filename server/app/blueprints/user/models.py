from app.extensions import db


class User(db.Model):
    __tablename__ = "users"
    ROLE = {"normal": "Normal", "admin": "Admin"}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, nullable=False, server_default="1")

    list_of_role_id = db.relationship("UserHasRoles", cascade="delete")
    list_of_extra_permissions_id = db.relationship("UserHasExtraPermission", cascade="delete")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        keys = data.keys()
        for key in keys:
            setattr(self, key, data[key])
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def authenticate(self, password):
        return self.password == password

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()
