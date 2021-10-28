from app import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def to_dict(self):
        post_dict = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date_created': self.date_created,
            'user_id': self.user_id
        }
        return post_dict

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_post(self, data):
        for field in data:
            if field in {'title', 'content'}:
                setattr(self, field, data[field])
        db.session.commit()
