from app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        self.title = data["title"]
        self.content = data["content"]
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
